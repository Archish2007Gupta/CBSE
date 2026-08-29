"""Service listing routes.

Endpoints
---------
GET /api/services
    Returns all services, optionally filtered by ``target_audience``.

    Optional query parameters
    -------------------------
    target_audience : str
        If provided, only services whose ``target_audience`` list contains
        this value are returned.
    role : str
        User role (student | parent | teacher | school).  When provided,
        services that are in that role's priority list are marked with
        ``priority: true`` and sorted to the **top** of the response.
        All other services are still returned with ``priority: false`` —
        nothing is hidden.

Priority mapping (by role)
--------------------------
student  → Results, Examinations, Student Services
parent   → Results, Examination Dates (Important Dates), Student Services
teacher  → Training / CTET, Academics, General Notices (circulars)
school   → Affiliation / School Services, Examinations, School Services
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query, status

from schemas.service import ServiceListResponse, ServiceResponse
from services import get_supabase_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/services", tags=["services"])

_SERVICE_FIELDS = "id,title,description,category,target_audience,url,icon,created_at"

# ---------------------------------------------------------------------------
# Role → priority category set
# Category strings must match the ``category`` field in the SERVICES data.
# ---------------------------------------------------------------------------
_ROLE_PRIORITY_CATEGORIES: dict[str, set[str]] = {
    "student": {"Results", "Examinations", "Student Services"},
    "parent": {"Results", "Student Services", "School Services"},
    "teacher": {"CTET", "Academics", "General Notices"},
    "school": {"School Services", "Examinations", "Affiliation"},
}


def _is_priority(service_category: str, role: str | None) -> bool:
    """Return True when *service_category* is in the priority set for *role*."""
    if role is None:
        return False
    priority_cats = _ROLE_PRIORITY_CATEGORIES.get(role.lower(), set())
    return service_category in priority_cats


@router.get("", response_model=ServiceListResponse)
def list_services(
    target_audience: str | None = Query(default=None, min_length=1, max_length=100),
    role: str | None = Query(
        default=None,
        description=(
            "User role: student | parent | teacher | school.  "
            "Priority services for this role are sorted first and marked "
            "priority=true.  All other services are still returned."
        ),
    ),
) -> ServiceListResponse:
    """Return all services, with role-based priority sorting when ``role`` is given.

    * **Priority services** — categories relevant to *role* — appear first,
      sorted alphabetically within the group, with ``priority=true``.
    * **Other services** — still returned, with ``priority=false`` — follow
      in alphabetical order so nothing is hidden.
    """
    try:
        query = get_supabase_client().table("services").select(_SERVICE_FIELDS)

        if target_audience is not None:
            query = query.contains("target_audience", [target_audience])

        response = query.execute()
        raw_services = response.data or []

        # Validate role value (ignore unknown values silently; don't 400)
        normalised_role: str | None = None
        if role is not None:
            role_lower = role.lower()
            if role_lower in _ROLE_PRIORITY_CATEGORIES:
                normalised_role = role_lower
            else:
                logger.warning("Unknown role value '%s' — priority sorting skipped.", role)

        # Annotate each service with priority flag
        annotated: list[ServiceResponse] = []
        for svc in raw_services:
            is_prio = _is_priority(svc.get("category", ""), normalised_role)
            annotated.append(ServiceResponse(**svc, priority=is_prio))

        # Sort: priority=True first, then by title alphabetically within each group
        annotated.sort(key=lambda s: (0 if s.priority else 1, s.title))

        return ServiceListResponse(records_retrieved=len(annotated), services=annotated)

    except Exception:
        logger.exception("Unable to retrieve services from Supabase")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service data is currently unavailable.",
        )
