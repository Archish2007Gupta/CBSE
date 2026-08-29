"""Request and response schemas for user-preference endpoints."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """Permitted roles for a CBSE portal user."""

    student = "student"
    parent = "parent"
    teacher = "teacher"
    school = "school"


class UserProfileUpdate(BaseModel):
    """Payload for PUT /api/user/profile.

    All fields are optional — send only the ones you wish to change.
    """

    role: UserRole | None = Field(
        None,
        description="User role: student | parent | teacher | school.",
    )
    class_name: str | None = Field(
        None,
        alias="class",
        max_length=20,
        description="Class or grade of the student (e.g. '10', 'XI-Science').",
    )
    school: str | None = Field(
        None,
        max_length=200,
        description="Name or affiliation code of the school.",
    )

    model_config = {"populate_by_name": True}


class UserProfileResponse(BaseModel):
    """Response payload for GET and PUT /api/user/profile."""

    role: UserRole | None = Field(None, description="Current user role.")
    class_name: str | None = Field(
        None,
        alias="class",
        description="Current class or grade.",
    )
    school: str | None = Field(None, description="Current school name.")

    model_config = {"populate_by_name": True}
