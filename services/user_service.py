"""Lightweight in-process user-preference store.

No authentication is implemented yet.  Preferences are held in a
module-level dictionary keyed by a session identifier (currently always
the string ``"default"`` so there is effectively one shared profile per
server process).  This is intentionally minimal and will be replaced with
a database-backed, per-user store when authentication is added.
"""

from __future__ import annotations

import threading
from typing import Any

# Module-level store.  Key: session_id (str).  Value: preference dict.
_store: dict[str, dict[str, Any]] = {}
_lock = threading.Lock()

_DEFAULT_SESSION = "default"


def get_profile(session_id: str = _DEFAULT_SESSION) -> dict[str, Any]:
    """Return the stored preferences for *session_id*.

    Returns an empty dict (all fields ``None``) when nothing has been saved.
    """
    with _lock:
        return dict(_store.get(session_id, {}))


def update_profile(
    updates: dict[str, Any],
    session_id: str = _DEFAULT_SESSION,
) -> dict[str, Any]:
    """Merge *updates* into the stored preferences for *session_id*.

    Only keys whose value is not ``None`` are written so callers can send
    a partial payload without erasing existing fields.

    Returns the full profile after the update.
    """
    with _lock:
        current = _store.setdefault(session_id, {})
        for key, value in updates.items():
            if value is not None:
                current[key] = value
        return dict(current)
