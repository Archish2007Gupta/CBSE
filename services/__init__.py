"""Reusable backend services for the CBSE FastAPI application."""

from .document_service import circular_to_document, circulars_to_documents
from .embedding_service import EMBEDDING_DIMENSION, get_embeddings
from .groq_service import get_groq_llm
from .ollama_service import detect_ollama_model, get_ollama_llm, is_ollama_running
from .rag_service import generate_rag_answer
from .retrieval_service import retrieve_relevant_circulars
from .summarize_service import summarize_circular
from .supabase_service import get_supabase_client
from .vector_store_service import get_vector_store

__all__ = [
    "EMBEDDING_DIMENSION",
    "circular_to_document",
    "circulars_to_documents",
    "detect_ollama_model",
    "generate_rag_answer",
    "get_embeddings",
    "get_groq_llm",
    "get_ollama_llm",
    "get_supabase_client",
    "get_vector_store",
    "is_ollama_running",
    "retrieve_relevant_circulars",
    "summarize_circular",
]
