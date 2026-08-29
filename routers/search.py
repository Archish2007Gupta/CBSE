"""Semantic AI and Keyword search routes across CBSE portal content."""

import logging
from collections.abc import Iterable

from fastapi import APIRouter, HTTPException, Query, status

from schemas.search import SearchResponse, SearchResultResponse
from services import get_supabase_client, retrieve_relevant_circulars
from services.mock_database import CIRCULARS, NEWS, SERVICES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["search"])

_RESULT_LIMIT_PER_COLUMN = 20


def _search_mock_list(items: list[dict], query: str, fields: tuple[str, ...]) -> list[dict]:
    query_lower = query.lower()
    matched = []
    for item in items:
        for field in fields:
            val = str(item.get(field, "") or "").lower()
            if query_lower in val:
                matched.append(item)
                break
    return matched


def _search_table(
    table: str,
    columns: Iterable[str],
    select_fields: str,
    keyword_pattern: str,
    raw_query: str,
) -> list[dict]:
    """Search listed text columns and de-duplicate matching records."""
    matches: dict[str, dict] = {}
    try:
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
        if matches:
            return list(matches.values())
    except Exception as e:
        logger.debug(f"Supabase search failed for table {table}, falling back to mock data: {e}")

    # Fallback to mock data if database returns empty or fails
    if table == "circulars":
        return _search_mock_list(CIRCULARS, raw_query, ("title", "description", "content"))
    elif table == "news":
        return _search_mock_list(NEWS, raw_query, ("title", "description"))
    elif table == "services":
        return _search_mock_list(SERVICES, raw_query, ("title", "description", "name"))
    return []


@router.get("", response_model=SearchResponse)
def search_content(
    q: str = Query(..., min_length=1, max_length=200),
    semantic: bool = Query(default=True),
) -> SearchResponse:
    """Perform a semantic AI and keyword search across circulars, news, and services."""
    query = q.strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Search query cannot be empty.",
        )

    results: list[SearchResultResponse] = []
    seen_titles: set[str] = set()
    seen_ids: set[str] = set()

    # 1. Semantic AI Search using Vector Embeddings & Similarity Search
    if semantic:
        try:
            semantic_matches = retrieve_relevant_circulars(query=query, top_k=6)
            for match in semantic_matches:
                cid = str(match.get("circular_id", ""))
                title = match.get("title", "").strip()

                if title in seen_titles or (cid and cid in seen_ids):
                    continue
                if cid:
                    seen_ids.add(cid)
                if title:
                    seen_titles.add(title)

                results.append(
                    SearchResultResponse(
                        id=cid or None,
                        type="circular",
                        title=title,
                        description=match.get("description") or (match.get("content", "")[:250] + "..."),
                        category=match.get("category") or "Academic",
                        date=str(match.get("publication_date") or "2026-08-26"),
                        source_url=match.get("source_url"),
                        document_url=match.get("source_url"),
                        similarity_score=match.get("similarity_score"),
                        match_type="semantic",
                    )
                )
        except Exception as err:
            logger.warning(f"Semantic search encountered an issue: {err}")

    # 2. Keyword Search
    keyword_pattern = f"%{query}%"
    try:
        circulars = _search_table(
            table="circulars",
            columns=("title", "description", "content"),
            select_fields="id,title,description,category,publish_date,source_url,document_url",
            keyword_pattern=keyword_pattern,
            raw_query=query,
        )
        news = _search_table(
            table="news",
            columns=("title", "description"),
            select_fields="id,title,description,category,publish_date,source_url",
            keyword_pattern=keyword_pattern,
            raw_query=query,
        )
        services = _search_table(
            table="services",
            columns=("title", "description"),
            select_fields="id,title,description,category,created_at,url",
            keyword_pattern=keyword_pattern,
            raw_query=query,
        )

        for rec in circulars:
            cid = str(rec.get("id", ""))
            title = rec.get("title", "").strip()
            if title in seen_titles or (cid and cid in seen_ids):
                continue
            if cid:
                seen_ids.add(cid)
            if title:
                seen_titles.add(title)

            results.append(
                SearchResultResponse(
                    id=cid or None,
                    type="circular",
                    title=title,
                    description=rec.get("description"),
                    category=rec.get("category", "General"),
                    date=str(rec.get("publish_date") or "2026-08-26"),
                    source_url=rec.get("source_url"),
                    document_url=rec.get("document_url"),
                    similarity_score=None,
                    match_type="keyword",
                )
            )

        for rec in news:
            cid = str(rec.get("id", ""))
            title = rec.get("title", "").strip()
            if title in seen_titles or (cid and cid in seen_ids):
                continue
            if cid:
                seen_ids.add(cid)
            if title:
                seen_titles.add(title)

            results.append(
                SearchResultResponse(
                    id=cid or None,
                    type="news",
                    title=title,
                    description=rec.get("description"),
                    category=rec.get("category", "News"),
                    date=str(rec.get("publish_date") or "2026-08-25"),
                    source_url=rec.get("source_url"),
                    document_url=None,
                    similarity_score=None,
                    match_type="keyword",
                )
            )

        for rec in services:
            cid = str(rec.get("id", ""))
            title = rec.get("title") or rec.get("name") or "CBSE Service"
            title = title.strip()
            if title in seen_titles or (cid and cid in seen_ids):
                continue
            if cid:
                seen_ids.add(cid)
            if title:
                seen_titles.add(title)

            results.append(
                SearchResultResponse(
                    id=cid or None,
                    type="service",
                    title=title,
                    description=rec.get("description"),
                    category=rec.get("category", "Services"),
                    date=str(rec.get("created_at") or rec.get("publish_date") or "2026-08-20"),
                    source_url=rec.get("url") or rec.get("source_url"),
                    document_url=None,
                    similarity_score=None,
                    match_type="keyword",
                )
            )

        return SearchResponse(
            success=True,
            query=query,
            records_retrieved=len(results),
            results=results,
        )
    except Exception as exc:
        logger.exception("Unable to perform portal search")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search is currently unavailable.",
        ) from exc

