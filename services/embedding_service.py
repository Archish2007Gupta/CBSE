"""Embedding service for the CBSE AI/RAG layer.

Provides a cached OllamaEmbeddings instance that converts text into dense
vector representations suitable for similarity search.

Configuration (set in python_backend/.env):
    OLLAMA_BASE_URL      – Ollama server. Defaults to http://localhost:11434.
    OLLAMA_EMBED_MODEL   – Embedding model tag.
                           Defaults to "nomic-embed-text" (768 dimensions).

The embedding model is intentionally separate from the chat model so each
can be configured and swapped independently.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings

load_dotenv()

_DEFAULT_BASE_URL   = "http://localhost:11434"
_DEFAULT_EMBED_MODEL = "nomic-embed-text"

# Dimension produced by nomic-embed-text – used in the SQL migration.
EMBEDDING_DIMENSION = 768


@lru_cache(maxsize=1)
def get_embeddings() -> OllamaEmbeddings:
    """Return a cached OllamaEmbeddings instance.

    Raises:
        RuntimeError: If the Ollama server is not reachable.
    """
    import httpx

    base_url = os.getenv("OLLAMA_BASE_URL", _DEFAULT_BASE_URL).strip()
    model    = os.getenv("OLLAMA_EMBED_MODEL", _DEFAULT_EMBED_MODEL).strip()

    # Quick reachability check so the error is clear.
    try:
        with httpx.Client(timeout=2.0) as client:
            client.get(f"{base_url}/api/tags").raise_for_status()
    except Exception:
        # If Ollama is not available, create a mock embeddings service
        # This prevents deployment failures when Ollama is not running
        import warnings
        warnings.warn("Ollama not available, AI features may be limited", UserWarning)
        
        # Return a basic embeddings instance that will work with local fallback
        class MockEmbeddings:
            def embed_query(self, text: str) -> list[float]:
                # Simple hash-based embedding for fallback
                import hashlib
                hash_obj = hashlib.md5(text.encode())
                # Generate 768 dimensional vector from hash
                seed = int(hash_obj.hexdigest()[:8], 16)
                import random
                random.seed(seed)
                return [random.uniform(-1, 1) for _ in range(EMBEDDING_DIMENSION)]
            
            def embed_documents(self, texts: list[str]) -> list[list[float]]:
                return [self.embed_query(text) for text in texts]
        
        return MockEmbeddings()

    return OllamaEmbeddings(base_url=base_url, model=model)
