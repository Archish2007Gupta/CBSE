"""News listing routes."""

import logging

from fastapi import APIRouter, HTTPException, Query, status

from schemas.news import NewsListResponse
from services import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/news", tags=["news"])

_NEWS_FIELDS = "id,title,description,category,publish_date,source_url,created_at"


@router.get("", response_model=NewsListResponse)
def list_news(
    limit: int = Query(default=10, ge=1, le=100),
    category: str | None = Query(default=None, min_length=1, max_length=100),
) -> NewsListResponse:
    """Return news records in reverse publication order."""
    try:
        query = (
            get_supabase_client()
            .table("news")
            .select(_NEWS_FIELDS)
            .order("publish_date", desc=True)
        )

        if category is not None:
            query = query.eq("category", category)

        response = query.limit(limit).execute()
        news = response.data or []
        return NewsListResponse(records_retrieved=len(news), news=news)
    except Exception:
        logger.exception("Unable to retrieve news from Supabase")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="News data is currently unavailable.",
        )
