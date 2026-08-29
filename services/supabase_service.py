"""Supabase client factory for the CBSE FastAPI backend.

Returns a MockSupabaseClient backed by in-memory demo data so the portal
works out-of-the-box without requiring live Supabase table migrations.
When real Supabase tables are provisioned, remove the mock import and
uncomment the create_client line below.
"""

import os

from services.mock_database import MockSupabaseClient


def get_supabase_client():
    """Return a client that reads from the in-memory demo dataset.

    To switch to a real Supabase backend, set SUPABASE_URL and
    SUPABASE_ANON_KEY environment variables and replace this function body
    with:
        from functools import lru_cache
        from supabase import create_client
        @lru_cache(maxsize=1)
        def get_supabase_client():
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_ANON_KEY")
            return create_client(url, key)
    """
    return MockSupabaseClient()
