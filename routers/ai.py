"""Router for AI-powered RAG Q&A endpoints."""

from __future__ import annotations

import logging
from fastapi import APIRouter, HTTPException, status

from schemas.ai import AISourceItem, AskRequest, AskResponse, SummarizeResponse
from services.rag_service import generate_rag_answer
from services.summarize_service import summarize_circular

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.post("/ask", response_model=AskResponse)
def ask_cbse_ai(payload: AskRequest) -> AskResponse:
    """Answer user questions using CBSE Retrieval-Augmented Generation (RAG).

    Accepts a user question, retrieves relevant CBSE circulars, and generates
    a grounded answer with source citations.
    """
    question = (payload.message or "").strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question message cannot be empty.",
        )

    try:
        rag_result = generate_rag_answer(question=question)
        answer_text = rag_result.get("answer", "")
        raw_sources = rag_result.get("sources", [])

        formatted_sources: list[AISourceItem] = []
        for src in raw_sources:
            formatted_sources.append(
                AISourceItem(
                    title=src.get("title", "CBSE Circular"),
                    date=str(src.get("publication_date", "") or ""),
                    source_url=src.get("source_url", "") or "",
                )
            )

        return AskResponse(
            answer=answer_text,
            sources=formatted_sources,
        )

    except Exception as error:
        import traceback
        logger.error(f"Error executing AI RAG workflow: {error}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the answer. Please try again later.",
        ) from error


@router.post("/summarize/{circular_id}", response_model=SummarizeResponse)
def summarize_circular_endpoint(circular_id: str) -> SummarizeResponse:
    """Generate a structured summary of a specific CBSE circular by ID.

    Retrieves the circular, extracts its key points, important dates, and
    required actions using the AI model without hallucinating details.
    """
    cleaned_id = (circular_id or "").strip()
    if not cleaned_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Circular ID cannot be empty.",
        )

    try:
        summary_result = summarize_circular(circular_id=cleaned_id)
        return SummarizeResponse(
            summary=summary_result.get("summary", ""),
            key_points=summary_result.get("key_points", []),
            important_dates=summary_result.get("important_dates", []),
            required_actions=summary_result.get("required_actions", []),
            source_url=summary_result.get("source_url"),
        )
    except ValueError as val_err:
        logger.warning(f"Circular not found for summarization: {val_err}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(val_err),
        ) from val_err
    except Exception as error:
        logger.error(f"Error generating circular summary: {error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the summary. Please try again later.",
        ) from error
