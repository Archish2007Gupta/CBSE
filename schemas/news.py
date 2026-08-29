"""Response schemas for news resources."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NewsResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    category: str
    publish_date: datetime
    source_url: str | None
    created_at: datetime


class NewsListResponse(BaseModel):
    success: bool = True
    records_retrieved: int
    news: list[NewsResponse]
