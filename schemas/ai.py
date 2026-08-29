"""Request and response schemas for AI RAG endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Payload for POST /api/ai/ask."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The question or prompt for the CBSE AI Assistant.",
        examples=["What is the revaluation process?"],
    )


class AISourceItem(BaseModel):
    """Source citation record attached to an AI answer."""

    title: str = Field(..., description="Title of the source CBSE circular.")
    date: str = Field("", description="Publication date of the circular (ISO-8601 or formatted date).")
    source_url: str = Field("", description="URL link to the official circular or notice.")


class AskResponse(BaseModel):
    """Response payload for POST /api/ai/ask."""

    answer: str = Field(..., description="Grounded AI response generated from CBSE context.")
    sources: list[AISourceItem] = Field(
        default_factory=list,
        description="List of source circular citations used to formulate the answer.",
    )


class SummarizeResponse(BaseModel):
    """Response payload for POST /api/ai/summarize/{id}."""

    summary: str = Field(..., description="Concise textual summary of the circular.")
    key_points: list[str] = Field(..., description="List of key points extracted from the circular.")
    important_dates: list[str] = Field(..., description="List of important dates mentioned in the circular.")
    required_actions: list[str] = Field(..., description="List of required actions for schools, students, or stakeholders.")
    source_url: str | None = Field(None, description="Official source URL of the circular.")
