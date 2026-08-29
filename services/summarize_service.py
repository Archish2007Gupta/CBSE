"""Summarization service for the CBSE AI layer using LangChain."""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from langchain_core.messages import SystemMessage, HumanMessage

from services.groq_service import get_groq_llm
from services.supabase_service import get_supabase_client

SUMMARIZE_SYSTEM_PROMPT = """You are an expert CBSE document analyst. Your task is to analyze the provided CBSE circular and produce a structured summary.

STRICT INSTRUCTIONS:
1. Extract the requested fields based ONLY on the provided circular content.
2. Do NOT invent dates, rules, actions, or details. If any field (such as important dates or required actions) is not specified or mentioned in the circular, explicitly list a single string: "None specified in the circular".
3. You must output the response in raw JSON format matching the following keys:
{
  "summary": "Concise textual summary of the circular.",
  "key_points": ["Key point 1", "Key point 2"],
  "important_dates": ["Date 1: event description", "Date 2: event description"],
  "required_actions": ["Action 1 for schools/students"]
}
4. Respond with ONLY the raw JSON block. Do not include markdown code block formatting (like ```json) or any introductory or concluding text.
"""

SUMMARIZE_USER_TEMPLATE = """CIRCULAR TITLE: {title}
CIRCULAR CATEGORY: {category}
PUBLICATION DATE: {publish_date}
CIRCULAR CONTENT:
{content}
"""


def _get_llm_instance():
    """Return the Groq chat model used for circular summarization."""
    return get_groq_llm()


def _clean_json_response(raw_text: str) -> dict[str, Any]:
    """Clean the raw LLM response text and parse it as JSON."""
    cleaned = raw_text.strip()
    # Strip thinking tags if returned by reasoning models
    cleaned = re.sub(r"<think>[\s\S]*?</think>", "", cleaned, flags=re.DOTALL).strip()
    # Strip markdown code blocks if the LLM outputted them
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: extract the outermost JSON object if surrounding text exists
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        raise ValueError(
            f"Failed to parse LLM response as JSON. Raw response: {raw_text}"
        )



def summarize_circular(
    circular_id: str,
) -> dict[str, Any]:
    """Retrieve a circular by ID, summarize its content using the LLM, and return structured info.

    Args:
        circular_id: UUID of the circular.
    Returns:
        Dict matching SummarizeResponse schema.
    """
    # 1. Retrieve the circular from Supabase
    client = get_supabase_client()
    response = client.table("circulars").select("*").eq("id", circular_id).execute()
    records = response.data or []

    if not records:
        raise ValueError(f"Circular with ID {circular_id} not found.")

    circular = records[0]

    # 2. Resolve LLM
    llm = _get_llm_instance()

    # 3. Format input content
    user_content = SUMMARIZE_USER_TEMPLATE.format(
        title=circular.get("title", "Untitled Circular"),
        category=circular.get("category", "General"),
        publish_date=circular.get("publish_date", "Unknown"),
        content=circular.get("content", ""),
    )

    # 4. Invoke LLM
    messages = [
        SystemMessage(content=SUMMARIZE_SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    try:
        llm_response = llm.invoke(messages)
    except Exception as exc:
        raise RuntimeError("Groq could not generate a circular summary at this time.") from exc
    raw_answer = str(llm_response.content).strip()

    # 5. Parse JSON summary output
    parsed = _clean_json_response(raw_answer)

    # Ensure required lists are formatted cleanly
    key_points = parsed.get("key_points") or ["None specified in the circular"]
    important_dates = parsed.get("important_dates") or ["None specified in the circular"]
    required_actions = parsed.get("required_actions") or ["None specified in the circular"]

    # Wrap lists if they are single strings
    if isinstance(key_points, str):
        key_points = [key_points]
    if isinstance(important_dates, str):
        important_dates = [important_dates]
    if isinstance(required_actions, str):
        required_actions = [required_actions]

    return {
        "summary": parsed.get("summary") or "No summary available.",
        "key_points": key_points,
        "important_dates": important_dates,
        "required_actions": required_actions,
        "source_url": circular.get("source_url"),
    }
