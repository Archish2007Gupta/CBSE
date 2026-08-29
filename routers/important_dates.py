"""Important-date listing routes."""

import logging
from datetime import date

from fastapi import APIRouter, HTTPException, Query, status

from schemas.important_dates import ImportantDateListResponse, ImportantDateResponse
from services import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/important-dates", tags=["important-dates"])

_IMPORTANT_DATE_FIELDS = (
    "id,title,description,event_date,category,target_audience,source_url,created_at"
)


@router.get("", response_model=ImportantDateListResponse)
def list_important_dates(
    limit: int = Query(default=10, ge=1, le=100),
) -> ImportantDateListResponse:
    """Return important dates ordered from earliest to latest event date."""
    try:
        response = (
            get_supabase_client()
            .table("important_dates")
            .select(_IMPORTANT_DATE_FIELDS)
            .order("event_date")
            .limit(limit)
            .execute()
        )

        today = date.today()
        important_dates = []
        for record in response.data or []:
            event_date = date.fromisoformat(record["event_date"])
            days_remaining = (event_date - today).days
            important_dates.append(
                ImportantDateResponse(
                    **record,
                    days_remaining=days_remaining,
                    event_status="past" if days_remaining < 0 else "upcoming",
                )
            )

        return ImportantDateListResponse(
            records_retrieved=len(important_dates),
            important_dates=important_dates,
        )
    except Exception:
        logger.exception("Unable to retrieve important dates from Supabase")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Important date data is currently unavailable.",
        )
