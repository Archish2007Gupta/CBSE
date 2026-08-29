"""Keyword search route across public CBSE portal content."""

import logging
from collections.abc import Iterable

from fastapi import APIRouter, HTTPException, Query, status

from schemas.search import SearchResponse, SearchResultResponse
from services import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["search"])

_RESULT_LIMIT_PER_COLUMN = 20


def _search_table(
    table: str,
    columns: Iterable[str],
    select_fields: str,
    keyword_pattern: str,
) -> list[dict]:
    """Search listed text columns and de-duplicate matching records by UUID."""
    matches: dict[str, dict] = {}
    client = get_supabase_client()

    for column in columns:
        response = (
            client.table(table)
            .select(select_fields)
            .ilike(column, keyword_pattern)
            .limit(_RESULT_LIMIT_PER_COLUMN)
            .execute()
        )
        for record in response.data or []:
            matches[record["id"]] = record

    return list(matches.values())


@router.get("", response_model=SearchResponse)
def search_content(
    q: str = Query(..., min_length=1, max_length=200),
) -> SearchResponse:
    """Perform a keyword search across circulars, news, and services."""
    query = q.strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Search query cannot be empty.",
        )

    keyword_pattern = f"%{query}%"

    try:
        circulars = _search_table(
            table="circulars",
            columns=("title", "description", "content"),
            select_fields=(
                "id,title,description,category,publish_date,source_url,document_url"
            ),
            keyword_pattern=keyword_pattern,
        )
        news = _search_table(
            table="news",
            columns=("title", "description"),
            select_fields="id,title,description,category,publish_date,source_url",
            keyword_pattern=keyword_pattern,
        )
        services = _search_table(
            table="services",
            columns=("title", "description"),
            select_fields="id,title,description,category,created_at,url",
            keyword_pattern=keyword_pattern,
        )

        results = [
            SearchResultResponse(
                id=str(record.get("id", "")),
                type="circular",
                title=record["title"],
                description=record.get("description"),
                category=record["category"],
                date=record["publish_date"],
                source_url=record.get("source_url"),
                document_url=record.get("document_url"),
            )
            for record in circulars
        ]
        results.extend(
            SearchResultResponse(
                id=str(record.get("id", "")),
                type="news",
                title=record["title"],
                description=record.get("description"),
                category=record["category"],
                date=record["publish_date"],
                source_url=record.get("source_url"),
                document_url=None,
            )
            for record in news
        )
        results.extend(
            SearchResultResponse(
                id=str(record.get("id", "")),
                type="service",
                title=record["title"],
                description=record.get("description"),
                category=record["category"],
                date=record["created_at"],
                source_url=record.get("url"),
                document_url=None,
            )
            for record in services
        )
        results.sort(key=lambda item: item.date, reverse=True)

        return SearchResponse(
            query=query,
            records_retrieved=len(results),
            results=results,
        )
    except Exception:
        logger.exception("Unable to search portal content through Supabase")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search is currently unavailable.",
        )
