"""
Autonomous Lab TA - Backend Application
FastAPI entry point with CORS, routers, and startup events.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.endpoints import auth, chat, submissions
from app.core.config import settings


# Path to frontend folder
FRONTEND_PATH = Path(__file__).parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: Initialize ChromaDB, load prompts, etc.
    print("🚀 Starting Autonomous Lab TA Backend...")
    print(f"📁 Frontend path: {FRONTEND_PATH}")
    if FRONTEND_PATH.exists():
        print("✅ Frontend found - serving at http://127.0.0.1:8000")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="Autonomous Lab TA",
    description="AI-powered teaching assistant for programming labs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins since frontend is served from same server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(submissions.router, prefix="/api/submissions", tags=["Submissions"])


@app.get("/")
async def serve_frontend():
    """Serve the frontend index.html at root."""
    index_path = FRONTEND_PATH / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "message": "Autonomous Lab TA API",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check for Docker/K8s."""
    return {"status": "healthy"}


# Mount static files for CSS, JS, etc. (must be after specific routes)
if FRONTEND_PATH.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_PATH), html=True), name="frontend")

