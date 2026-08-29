"""Groq LLM service for the CBSE FastAPI backend.

Provides a cached ChatGroq instance that can be imported and used by any
router or service that needs LLM capabilities.

Configuration (set in python_backend/.env or as shell environment variables):
    GROQ_API_KEY   – Secret key from https://console.groq.com/keys
    GROQ_MODEL     – (Optional) Groq model ID.
                     Defaults to "llama-3.3-70b-versatile".
    GROQ_TEMPERATURE – (Optional) Sampling temperature, 0–2. Defaults to 0.
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load variables from python_backend/.env (no-op when running in production
# environments where variables are already injected).
load_dotenv()

_DEFAULT_MODEL = "qwen/qwen3.6-27b"
_DEFAULT_TEMPERATURE = 0


@lru_cache(maxsize=1)
def get_groq_llm() -> ChatGroq:
    """Return a cached ChatGroq instance.

    Raises:
        EnvironmentError: If GROQ_API_KEY is not set.
    """
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. "
            "Add it to python_backend/.env or export it as an environment variable."
        )

    model = os.getenv("GROQ_MODEL", _DEFAULT_MODEL).strip()
    temperature = float(os.getenv("GROQ_TEMPERATURE", str(_DEFAULT_TEMPERATURE)))

    return ChatGroq(
        api_key=api_key,
        model=model,
        temperature=temperature,
    )
