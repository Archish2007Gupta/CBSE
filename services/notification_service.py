"""Lightweight in-process notification store.

No authentication is implemented yet.  All requests share the single
``"default"`` session, exactly like the user-preference store.

The store is seeded once with realistic-looking demo notifications so
the GET endpoint is immediately usable in the prototype.  Notifications
persist for the lifetime of the server process; a PUT /read call simply
flips ``read=True`` in memory.

When auth is added, replace ``_DEFAULT_SESSION`` lookups with the real
user-id extracted from the JWT/session token.
"""

from __future__ import annotations

import threading
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Seed data — one realistic demo notification per major category.
# Timestamps are fixed so the list is deterministic across restarts.
# ---------------------------------------------------------------------------
def _ts(date_str: str) -> str:
    """Return an ISO-8601 UTC timestamp string for a YYYY-MM-DD date."""
    return datetime.fromisoformat(date_str).replace(
        hour=9, minute=0, second=0, tzinfo=timezone.utc
    ).isoformat()


_SEED_NOTIFICATIONS: list[dict[str, Any]] = [
    {
        "id": str(uuid.UUID("60000000-0000-4000-8000-000000000001")),
        "title": "Board Examination Results Published",
        "message": (
            "Class X and XII board examination results for 2026 are now available. "
            "Log in to the results portal to view your marks and download your digital marksheet."
        ),
        "category": "Results",
        "priority": "high",
        "created_at": _ts("2026-08-26"),
        "read": False,
    },
    {
        "id": str(uuid.UUID("60000000-0000-4000-8000-000000000002")),
        "title": "Admit Card Download Window Open",
        "message": (
            "Admit cards for the supplementary examinations are available for download. "
            "Schools must distribute verified cards to candidates before the examination date."
        ),
        "category": "Examinations",
        "priority": "high",
        "created_at": _ts("2026-08-20"),
        "read": False,
    },
    {
        "id": str(uuid.UUID("60000000-0000-4000-8000-000000000003")),
        "title": "Re-evaluation Application Deadline Approaching",
        "message": (
            "The deadline to apply for marks verification and re-evaluation is 28 August 2026. "
            "Submit your application through the Re-evaluation Portal before the window closes."
        ),
        "category": "Results",
        "priority": "medium",
        "created_at": _ts("2026-08-18"),
        "read": False,
    },
    {
        "id": str(uuid.UUID("60000000-0000-4000-8000-000000000004")),
        "title": "New Curriculum Enrichment Circular Released",
        "message": (
            "CBSE has published updated curriculum enrichment activity guidelines for 2026-27. "
            "Schools and teachers are requested to review the circular and plan accordingly."
        ),
        "category": "Circulars",
        "priority": "medium",
        "created_at": _ts("2026-08-21"),
        "read": False,
    },
    {
        "id": str(uuid.UUID("60000000-0000-4000-8000-000000000005")),
        "title": "CTET Online Applications Open",
        "message": (
            "Online applications for the Central Teacher Eligibility Test (CTET) are now open. "
            "Eligible candidates may apply at ctet.nic.in before the closing date."
        ),
        "category": "CTET",
        "priority": "medium",
        "created_at": _ts("2026-08-12"),
        "read": True,   # pre-read so the unread count is realistic
    },
    {
        "id": str(uuid.UUID("60000000-0000-4000-8000-000000000006")),
        "title": "Sample Question Papers Available",
        "message": (
            "Updated sample question papers and marking schemes for Classes X and XII "
            "are available on the Academic Resources portal. Useful for examination preparation."
        ),
        "category": "Academics",
        "priority": "low",
        "created_at": _ts("2026-08-12"),
        "read": True,
    },
    {
        "id": str(uuid.UUID("60000000-0000-4000-8000-000000000007")),
        "title": "School Data Verification Window",
        "message": (
            "Affiliated schools are requested to verify and update their institutional data "
            "in the CBSE management portal before 15 September 2026."
        ),
        "category": "School Services",
        "priority": "low",
        "created_at": _ts("2026-08-03"),
        "read": True,
    },
]

# ---------------------------------------------------------------------------
# In-memory store  — { session_id: [ notification_dict, ... ] }
# ---------------------------------------------------------------------------
_store: dict[str, list[dict[str, Any]]] = {}
_lock = threading.Lock()

_DEFAULT_SESSION = "default"


def _init_session(session_id: str) -> None:
    """Seed the session store with a deep copy of the demo notifications."""
    if session_id not in _store:
        _store[session_id] = deepcopy(_SEED_NOTIFICATIONS)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_notifications(session_id: str = _DEFAULT_SESSION) -> list[dict[str, Any]]:
    """Return all notifications for *session_id*, newest first."""
    with _lock:
        _init_session(session_id)
        notifications = list(_store[session_id])

    # Sort by created_at descending
    notifications.sort(key=lambda n: n["created_at"], reverse=True)
    return notifications


def mark_read(
    notification_id: str,
    session_id: str = _DEFAULT_SESSION,
) -> dict[str, Any] | None:
    """Set ``read=True`` on the matching notification.

    Returns the updated notification dict, or ``None`` if not found.
    """
    with _lock:
        _init_session(session_id)
        for notif in _store[session_id]:
            if notif["id"] == notification_id:
                notif["read"] = True
                return dict(notif)
    return None
