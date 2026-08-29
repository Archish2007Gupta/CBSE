"""Response schemas for keyword search resources."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class SearchResultResponse(BaseModel):
    id: str | None = None
    type: Literal["circular", "news", "service"]
    title: str
    description: str | None
    category: str
    date: datetime
    source_url: str | None
    document_url: str | None


class SearchResponse(BaseModel):
    success: bool = True
    query: str
    records_retrieved: int
    results: list[SearchResultResponse]
