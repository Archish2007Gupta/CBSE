"""Request and response schemas for notification endpoints."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class NotificationPriority(str, Enum):
    """Urgency level of a notification."""

    high = "high"
    medium = "medium"
    low = "low"


class NotificationResponse(BaseModel):
    """A single notification as returned by GET /api/notifications."""

    id: UUID
    title: str
    message: str
    category: str = Field(description="Topic area, e.g. 'Results', 'Examinations'.")
    priority: NotificationPriority
    created_at: datetime
    read: bool = Field(False, description="True once the user has marked this notification read.")


class NotificationListResponse(BaseModel):
    """Response envelope for GET /api/notifications."""

    success: bool = True
    total: int = Field(description="Total notifications returned.")
    unread: int = Field(description="Number of unread notifications.")
    notifications: list[NotificationResponse]
