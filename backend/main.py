"""
Autonomous Lab TA - Backend Application
FastAPI entry point with CORS, routers, and startup events.
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import auth, chat, submissions
from app.core.config import settings


# Path to frontend folder
FRONTEND_PATH = Path(__file__).parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: Initialize ChromaDB, load prompts, etc.
    print("🚀 Starting Autonomous Lab TA Backend...")
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
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(submissions.router, prefix="/api/submissions", tags=["Submissions"])

# Mount static files for debug frontend
if FRONTEND_PATH.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_PATH)), name="static")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Autonomous Lab TA API",
        "status": "running",
        "docs": "/docs",
        "debug_frontend": "/static/index.html"
    }


@app.get("/health")
async def health_check():
    """Health check for Docker/K8s."""
    return {"status": "healthy"}
