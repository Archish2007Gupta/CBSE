"""Response schemas for service resources."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ServiceResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    category: str
    target_audience: list[str]
    url: str
    icon: str | None
    created_at: datetime
    priority: bool = Field(
        False,
        description=(
            "True when this service is in the priority list for the requested user role. "
            "Priority services are always returned first."
        ),
    )


class ServiceListResponse(BaseModel):
    success: bool = True
    records_retrieved: int
    services: list[ServiceResponse]
