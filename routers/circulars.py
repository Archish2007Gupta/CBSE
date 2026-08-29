"""Circular listing routes."""

import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from schemas.circular import CircularListResponse, CircularResponse
from services import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/circulars", tags=["circulars"])

_CIRCULAR_FIELDS = (
    "id,title,description,content,category,target_audience,"
    "publish_date,document_url,source_url,created_at"
)


@router.get("", response_model=CircularListResponse)
def list_circulars(
    limit: int = Query(default=10, ge=1, le=100),
    category: str | None = Query(default=None, min_length=1, max_length=100),
) -> CircularListResponse:
    """Return circulars in reverse publication order."""
    try:
        query = (
            get_supabase_client()
            .table("circulars")
            .select(_CIRCULAR_FIELDS)
            .order("publish_date", desc=True)
        )

        if category is not None:
            query = query.eq("category", category)

        response = query.limit(limit).execute()
        circulars = response.data or []
        return CircularListResponse(
            records_retrieved=len(circulars),
            circulars=circulars,
        )
    except Exception:
        logger.exception("Unable to retrieve circulars from Supabase")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Circular data is currently unavailable.",
        )


@router.get("/{circular_id}", response_model=CircularResponse)
def get_circular(circular_id: UUID) -> CircularResponse:
    """Return one circular by its UUID."""
    try:
        response = (
            get_supabase_client()
            .table("circulars")
            .select(_CIRCULAR_FIELDS)
            .eq("id", str(circular_id))
            .limit(1)
            .execute()
        )
        circulars = response.data or []

        if not circulars:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Circular not found.",
            )

        return CircularResponse.model_validate(circulars[0])
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unable to retrieve circular %s from Supabase", circular_id)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Circular data is currently unavailable.",
        )
