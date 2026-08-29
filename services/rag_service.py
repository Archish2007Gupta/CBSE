"""Core RAG service for the CBSE AI layer using LangChain.

Workflow:
  User Question
    └──> Retrieve relevant CBSE circular documents (via retrieval_service)
    └──> Format retrieved documents into grounded context
    └──> Construct strict system & human prompt (zero-hallucination guardrails)
    └──> Invoke Groq LLM
    └──> Return structured answer + citations

Prompt Rules:
  - Answer ONLY from retrieved CBSE context.
  - Do NOT invent dates, rules, or procedures.
  - Clearly state when information cannot be verified from the retrieved context.
"""

from __future__ import annotations

import os
import re
from typing import Any, Optional

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from services.groq_service import get_groq_llm
from services.retrieval_service import retrieve_relevant_circulars

load_dotenv()

RAG_SYSTEM_PROMPT = """You are the official CBSE AI Assistant. Your responsibility is to answer user questions accurately based ONLY on the official CBSE context provided below.

STRICT INSTRUCTIONS:
1. Answer ONLY using the information explicitly stated in the retrieved CBSE context below.
2. Do NOT invent, assume, or extrapolate any dates, fee amounts, eligibility criteria, rules, or procedures that are not explicitly present in the context.
3. If the retrieved context does not contain enough information to answer the question, clearly state: "Based on the official CBSE circulars available, this information cannot be verified."
4. Be helpful, clear, and professional.
5. Cite the circular title or source URL when citing specific rules or guidelines.
"""

RAG_USER_TEMPLATE = """RETRIEVED CBSE CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:"""


def _format_context(retrieved_circulars: list[dict[str, Any]]) -> str:
    """Format retrieved circular dicts into a readable context block for the LLM."""
    if not retrieved_circulars:
        return "No relevant CBSE circulars found in the database."

    blocks = []
    for idx, c in enumerate(retrieved_circulars, 1):
        block_lines = [
            f"--- CIRCULAR #{idx} ---",
            f"Title: {c.get('title', 'N/A')}",
            f"Category: {c.get('category', 'N/A')}",
            f"Target Audience: {c.get('target_audience', 'N/A')}",
            f"Publication Date: {c.get('publication_date', 'N/A')}",
            f"Description: {c.get('description', '')}",
            f"Content: {c.get('content', '')}",
        ]
        if c.get("source_url"):
            block_lines.append(f"Source URL: {c['source_url']}")
        blocks.append("\n".join(block_lines))

    return "\n\n".join(blocks)


def _get_llm_instance():
    """Return the Groq chat model used for RAG answer generation.

    Embeddings are intentionally handled separately by ``embedding_service``;
    this function must never require a local Ollama chat model.
    """
    return get_groq_llm(), "groq"


def generate_rag_answer(
    question: str,
    top_k: int = 4,
    category_filter: Optional[str] = None,
) -> dict[str, Any]:
    """Execute full RAG workflow for a user question.

    Args:
        question: User's query string.
        top_k: Number of relevant circular documents to retrieve.
        category_filter: Optional category restriction.

    Returns:
        Structured dict containing:
          - question (str)
          - answer (str)
          - sources (list of dicts)
          - provider (str)
          - model_name (str)
          - retrieved_count (int)
    """
    cleaned_question = (question or "").strip()
    if not cleaned_question:
        return {
            "question": "",
            "answer": "Please provide a valid question.",
            "sources": [],
            "provider": "groq",
            "model_name": "none",
            "retrieved_count": 0,
        }

    # 1. Retrieve relevant CBSE circulars
    retrieved_circulars = retrieve_relevant_circulars(
        cleaned_question,
        top_k=top_k,
        category_filter=category_filter,
    )

    # 2. Build grounded context
    formatted_context = _format_context(retrieved_circulars)

    # 3. Resolve the Groq LLM. Retrieval and prompt construction remain unchanged.
    llm, resolved_provider = _get_llm_instance()
    model_name = getattr(llm, "model_name", getattr(llm, "model", "unknown"))

    # 4. Construct prompt and send to LLM
    messages = [
        SystemMessage(content=RAG_SYSTEM_PROMPT),
        HumanMessage(content=RAG_USER_TEMPLATE.format(
            context=formatted_context,
            question=cleaned_question,
        )),
    ]

    try:
        response = llm.invoke(messages)
    except Exception as exc:
        raise RuntimeError("Groq could not generate an answer at this time.") from exc
    answer_text = str(response.content).strip()
    answer_text = re.sub(r"<think>[\s\S]*?</think>", "", answer_text, flags=re.DOTALL).strip()

    # 5. Extract citation sources
    sources = [
        {
            "rank": c["rank"],
            "title": c["title"],
            "category": c["category"],
            "source_url": c.get("source_url", ""),
            "publication_date": c.get("publication_date", ""),
            "similarity_score": c.get("similarity_score", 0.0),
        }
        for c in retrieved_circulars
    ]

    return {
        "question": cleaned_question,
        "answer": answer_text,
        "sources": sources,
        "provider": resolved_provider,
        "model_name": model_name,
        "retrieved_count": len(retrieved_circulars),
    }
