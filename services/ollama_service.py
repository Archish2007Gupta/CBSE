"""Ollama LLM service for the CBSE FastAPI backend.

Provides a locally-running ChatOllama instance via LangChain.
Ollama is entirely optional — the application starts and functions normally
without it.  Only activate this service when a local model is needed (e.g.
for offline development or as a fallback when no Groq API key is available).

Configuration (set in python_backend/.env or as shell environment variables):
    OLLAMA_BASE_URL   – Ollama server address.
                        Defaults to "http://localhost:11434".
    OLLAMA_MODEL      – Model tag to use (must already be pulled).
                        Defaults to auto-detected first available model.
    OLLAMA_TEMPERATURE – Sampling temperature, 0–2. Defaults to 0.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import httpx
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load variables from python_backend/.env
load_dotenv()

_DEFAULT_BASE_URL = "http://localhost:11434"
_DEFAULT_TEMPERATURE = 0


# ---------------------------------------------------------------------------
# Availability helpers
# ---------------------------------------------------------------------------

def is_ollama_running(base_url: str = _DEFAULT_BASE_URL) -> bool:
    """Return True if the Ollama HTTP server is reachable."""
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=3.0)
        return response.status_code == 200
    except Exception:
        return False


def list_ollama_models(base_url: str = _DEFAULT_BASE_URL) -> list[str]:
    """Return a list of locally available Ollama model names.

    Returns an empty list if Ollama is not running or has no models.
    """
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=3.0)
        response.raise_for_status()
        data = response.json()
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def detect_ollama_model(base_url: str = _DEFAULT_BASE_URL) -> Optional[str]:
    """Return the first available local Ollama model, or None."""
    models = list_ollama_models(base_url)
    return models[0] if models else None


# ---------------------------------------------------------------------------
# Service factory
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_ollama_llm() -> ChatOllama:
    """Return a cached ChatOllama instance pointed at the local Ollama server.

    Raises:
        RuntimeError: If Ollama is not reachable or no models are available.
    """
    base_url = os.getenv("OLLAMA_BASE_URL", _DEFAULT_BASE_URL).strip()
    temperature = float(os.getenv("OLLAMA_TEMPERATURE", str(_DEFAULT_TEMPERATURE)))

    if not is_ollama_running(base_url):
        raise RuntimeError(
            f"Ollama server is not reachable at {base_url}. "
            "Start Ollama with `ollama serve` and ensure at least one model "
            "is pulled (e.g. `ollama pull qwen2:7b`)."
        )

    # Resolve model: env var takes precedence, otherwise auto-detect.
    model = os.getenv("OLLAMA_MODEL", "").strip()
    if not model:
        model = detect_ollama_model(base_url)
    if not model:
        raise RuntimeError(
            "No Ollama models found. Pull one first, e.g.: ollama pull qwen2:7b"
        )

    return ChatOllama(
        base_url=base_url,
        model=model,
        temperature=temperature,
    )
