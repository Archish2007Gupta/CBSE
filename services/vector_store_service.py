"""Supabase pgvector store service for the CBSE AI/RAG layer.

Wraps LangChain's SupabaseVectorStore to provide a ready-to-use retrieval
interface backed by Supabase + pgvector.

Table schema (apply database/migrations/001_pgvector_circulars.sql first):
    circular_embeddings (id, content, metadata, embedding)

Configuration (set in python_backend/.env):
    SUPABASE_URL       – Project URL from the Supabase dashboard.
    SUPABASE_ANON_KEY  – Anon/public key (safe for server-side use).
    VECTOR_TABLE       – Table name. Defaults to "circular_embeddings".
    VECTOR_QUERY_FN    – RPC function for similarity search.
                         Defaults to "match_circular_embeddings".
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.embeddings import Embeddings
from supabase import create_client, Client

load_dotenv()

_DEFAULT_TABLE    = "circular_embeddings"
_DEFAULT_QUERY_FN = "match_circular_embeddings"


def _get_supabase_client() -> Client:
    """Create a Supabase client from environment variables.

    Raises:
        EnvironmentError: If SUPABASE_URL or SUPABASE_ANON_KEY is not set.
    """
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_ANON_KEY", "").strip()
    if not url or not key:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_ANON_KEY must be set in python_backend/.env "
            "to use the pgvector store."
        )
    return create_client(url, key)


def get_vector_store(embeddings: Embeddings) -> SupabaseVectorStore:
    """Return a SupabaseVectorStore connected to the circular_embeddings table.

    Args:
        embeddings: An initialised LangChain Embeddings instance (e.g. from
                    ``embedding_service.get_embeddings()``).

    Returns:
        A ``SupabaseVectorStore`` ready for ``add_documents`` and
        ``similarity_search`` calls.

    Raises:
        EnvironmentError: If Supabase credentials are missing.
        Exception: If the pgvector table or function does not exist yet
                   (run the SQL migration first).
    """
    table    = os.getenv("VECTOR_TABLE", _DEFAULT_TABLE)
    query_fn = os.getenv("VECTOR_QUERY_FN", _DEFAULT_QUERY_FN)
    client   = _get_supabase_client()

    return SupabaseVectorStore(
        client=client,
        embedding=embeddings,
        table_name=table,
        query_name=query_fn,
    )
