"""Response schemas for circular resources."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CircularResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    content: str | None
    category: str
    target_audience: list[str]
    publish_date: datetime
    document_url: str | None
    source_url: str | None
    created_at: datetime


class CircularListResponse(BaseModel):
    success: bool = True
    records_retrieved: int
    circulars: list[CircularResponse]
