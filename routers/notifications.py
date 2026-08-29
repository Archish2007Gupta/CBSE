"""Router for notification endpoints.

Endpoints
---------
GET  /api/notifications
    Return all notifications for the prototype user, newest first.
    Optional query parameter ``unread_only=true`` restricts results to
    unread notifications only.

PUT  /api/notifications/{id}/read
    Mark a single notification as read.  Returns the updated notification.

Authentication is not implemented yet.  All requests share the single
``"default"`` session (one shared inbox per server process).
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query, status

from schemas.notification import NotificationListResponse, NotificationResponse
from services.notification_service import get_notifications, mark_read

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationListResponse)
def list_notifications(
    unread_only: bool = Query(
        False,
        description="When true, only unread notifications are returned.",
    ),
) -> NotificationListResponse:
    """Return notifications for the current user, newest first.

    * ``total``  — count of notifications in the response.
    * ``unread`` — count of unread notifications across **all** stored
      notifications (independent of the ``unread_only`` filter), so the
      client always knows the badge count.
    """
    try:
        all_notifications = get_notifications()

        # Badge count is always based on the full set
        unread_count = sum(1 for n in all_notifications if not n["read"])

        if unread_only:
            visible = [n for n in all_notifications if not n["read"]]
        else:
            visible = all_notifications

        records = [NotificationResponse(**n) for n in visible]
        return NotificationListResponse(
            total=len(records),
            unread=unread_count,
            notifications=records,
        )
    except Exception as error:
        logger.error("Failed to retrieve notifications: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve notifications.",
        ) from error


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(notification_id: str) -> NotificationResponse:
    """Mark a notification as read and return the updated record.

    Returns **200** with the updated notification.
    Returns **404** if no notification with the given ID exists.
    Calling this on an already-read notification is idempotent (returns 200).
    """
    try:
        updated = mark_read(notification_id)
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification '{notification_id}' not found.",
            )
        return NotificationResponse(**updated)
    except HTTPException:
        raise
    except Exception as error:
        logger.error("Failed to mark notification as read: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update notification.",
        ) from error
