"""Document conversion service for the CBSE AI/RAG layer.

Converts raw circular records (dicts from MockSupabaseClient or real Supabase)
into LangChain ``Document`` objects ready for retrieval pipelines.

Each ``Document`` has:
  * ``page_content`` – a rich, human-readable text block assembled from the
    circular's title, description, and content fields.  This is what the
    retriever will search and what the LLM will read.
  * ``metadata``     – structured key/value pairs for filtering and citation:
      - title            (str)
      - description      (str)
      - category         (str)
      - target_audience  (str  – comma-separated list)
      - publication_date (str  – ISO-8601)
      - source_url       (str | "")
      - source           (str  – alias for source_url, LangChain convention)
      - circular_id      (str)

No embeddings are generated here.  This service is the single point where
circular data is normalised before it enters the vector store or LLM prompt.
"""

from __future__ import annotations

from typing import Any

from langchain_core.documents import Document


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def circular_to_document(circular: dict[str, Any]) -> Document:
    """Convert a single circular dict to a LangChain Document.

    Args:
        circular: A raw circular record with the fields produced by
                  MockSupabaseClient (or a live Supabase query).

    Returns:
        A ``langchain_core.documents.Document`` instance whose
        ``page_content`` is suitable for embedding / similarity search.
    """
    title       = (circular.get("title") or "").strip()
    description = (circular.get("description") or "").strip()
    content     = (circular.get("content") or "").strip()
    category    = (circular.get("category") or "").strip()
    source_url  = (circular.get("source_url") or "").strip()

    # target_audience may be a list or a comma-separated string.
    raw_audience = circular.get("target_audience") or []
    if isinstance(raw_audience, list):
        audience_str = ", ".join(raw_audience)
    else:
        audience_str = str(raw_audience).strip()

    # Normalise the publication date to a plain ISO-8601 string.
    publish_date = _normalise_date(circular.get("publish_date"))

    # Build a single, information-dense text block.  Ordering matters: the
    # most identifying information comes first so that both keyword search and
    # semantic search work well.
    page_content_parts: list[str] = []
    if title:
        page_content_parts.append(f"Title: {title}")
    if category:
        page_content_parts.append(f"Category: {category}")
    if audience_str:
        page_content_parts.append(f"Target Audience: {audience_str}")
    if publish_date:
        page_content_parts.append(f"Publication Date: {publish_date}")
    if description:
        page_content_parts.append(f"Description: {description}")
    if content:
        page_content_parts.append(f"Content: {content}")
    if source_url:
        page_content_parts.append(f"Source URL: {source_url}")

    page_content = "\n".join(page_content_parts)

    metadata: dict[str, Any] = {
        "circular_id":       str(circular.get("id", "")),
        "title":             title,
        "description":       description,
        "category":          category,
        "target_audience":   audience_str,
        "publication_date":  publish_date,
        "source_url":        source_url,
        # LangChain's built-in citation attribute
        "source":            source_url,
    }

    return Document(page_content=page_content, metadata=metadata)


def circulars_to_documents(circulars: list[dict[str, Any]]) -> list[Document]:
    """Convert a list of circular dicts to a list of LangChain Documents.

    Skips any circular that has neither a title nor content so that empty
    records do not pollute the retrieval index.

    Args:
        circulars: List of raw circular records.

    Returns:
        List of ``Document`` objects, one per valid circular.
    """
    documents: list[Document] = []
    for circular in circulars:
        title   = (circular.get("title") or "").strip()
        content = (circular.get("content") or "").strip()
        if not title and not content:
            continue
        documents.append(circular_to_document(circular))
    return documents


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _normalise_date(value: Any) -> str:
    """Return a consistent ISO-8601 date string regardless of input type."""
    if value is None:
        return ""
    # Already a string (most common from mock/Supabase JSON).
    if isinstance(value, str):
        return value.strip()
    # datetime / date objects.
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value).strip()
