"""Response schemas for important-date resources."""

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class ImportantDateResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    event_date: date
    category: str
    target_audience: list[str]
    source_url: str | None
    created_at: datetime
    days_remaining: int
    event_status: Literal["past", "upcoming"]


class ImportantDateListResponse(BaseModel):
    success: bool = True
    records_retrieved: int
    important_dates: list[ImportantDateResponse]
