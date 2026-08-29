"""Router for user-preference endpoints.

Endpoints
---------
GET  /api/user/profile  -- retrieve current profile preferences
PUT  /api/user/profile  -- update one or more preference fields

Authentication is not implemented yet.  All requests share a single
default session so the store behaves like a global scratchpad for now.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from schemas.user import UserProfileResponse, UserProfileUpdate
from services.user_service import get_profile, update_profile

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/user", tags=["User"])


@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile() -> UserProfileResponse:
    """Return the current user-preference profile.

    All fields default to ``null`` until a PUT request sets them.
    """
    try:
        data = get_profile()
        return UserProfileResponse(
            role=data.get("role"),
            class_name=data.get("class_name"),
            school=data.get("school"),
        )
    except Exception as error:
        logger.error("Failed to retrieve user profile: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve user profile.",
        ) from error


@router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(payload: UserProfileUpdate) -> UserProfileResponse:
    """Update one or more fields of the user-preference profile.

    Only fields that are explicitly provided (not ``null``) will overwrite
    the stored value.  Send a partial payload to change a single field.
    """
    try:
        # Build an update dict using internal field names.
        # ``class_name`` is the Python name; the JSON alias is ``"class"``.
        updates: dict = {}
        if payload.role is not None:
            updates["role"] = payload.role.value
        if payload.class_name is not None:
            updates["class_name"] = payload.class_name
        if payload.school is not None:
            updates["school"] = payload.school

        if not updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields were provided for update.",
            )

        updated = update_profile(updates)
        return UserProfileResponse(
            role=updated.get("role"),
            class_name=updated.get("class_name"),
            school=updated.get("school"),
        )
    except HTTPException:
        raise
    except Exception as error:
        logger.error("Failed to update user profile: %s", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update user profile.",
        ) from error
