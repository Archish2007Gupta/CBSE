import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""CBSE FastAPI application — serves both the backend API and the frontend static files."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers.circulars import router as circulars_router
from routers.important_dates import router as important_dates_router
from routers.news import router as news_router
from routers.search import router as search_router
from routers.services import router as services_router
from routers.ai import router as ai_router
from routers.user import router as user_router
from routers.notifications import router as notifications_router
from services import get_supabase_client

# Absolute path to the directory that contains index.html, styles.css, etc.
FRONTEND_DIR = Path(__file__).parent

app = FastAPI(
    title="CBSE Backend API",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

# Resolve allowed CORS origins from FRONTEND_URL environment variable
frontend_url_env = os.getenv("FRONTEND_URL", "").strip()

if frontend_url_env:
    # Production / explicitly configured frontend origins (supports comma-separated URLs)
    origins = [url.strip() for url in frontend_url_env.split(",") if url.strip()]
    allow_credentials = False if "*" in origins else True
else:
    # Local development fallback
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:5173",
        "http://localhost:5500",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "*",
    ]
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(circulars_router)
app.include_router(important_dates_router)
app.include_router(news_router)
app.include_router(search_router)
app.include_router(services_router)
app.include_router(ai_router)
app.include_router(user_router)
app.include_router(notifications_router)


@app.get("/api/test-db")
def test_database_connection() -> dict[str, int | bool]:
    """Verify database access by reading a small sample of circulars."""
    try:
        response = get_supabase_client().table("circulars").select("id").limit(5).execute()
        records = response.data or []
        return {"success": True, "recordsRetrieved": len(records)}
    except Exception as error:
        # Do not expose provider details or configuration values to clients.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The database is currently unavailable."
        ) from error


# ── Frontend HTML routes ──────────────────────────────────────────────────────
# These must come AFTER all /api/* routes so API calls are never intercepted.

@app.get("/", response_class=FileResponse)
def serve_index():
    """Serve the main CBSE website homepage."""
    return FileResponse(FRONTEND_DIR / "index.html", media_type="text/html")


@app.get("/sitemap", response_class=FileResponse)
@app.get("/sitemap.html", response_class=FileResponse)
def serve_sitemap():
    """Serve the sitemap page."""
    return FileResponse(FRONTEND_DIR / "sitemap.html", media_type="text/html")


# ── Static assets (CSS, JS, images) ──────────────────────────────────────────
# Mount at root so that relative paths in HTML (e.g. href="styles.css") work.
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")


# ── Entry point ───────────────────────────────────────────────────────────────
# Allows running the server with:  python main.py
# (equivalent to: uvicorn main:app --reload --host 127.0.0.1 --port 8000)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,          # auto-restarts when you save a file
        log_level="info",
    )
