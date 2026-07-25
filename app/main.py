"""Project Fifty — Multi-Agent Climate Intelligence Platform."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import close_db, init_db
from app.api.routes import router

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("project_fifty")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    logger.info("Starting Project Fifty v%s", settings.PROJECT_VERSION)
    try:
        await init_db()
        logger.info("Database tables created")
    except Exception as exc:
        logger.warning("Database init skipped (will retry): %s", exc)

    from app.services.scheduler import start_scheduler, stop_scheduler
    start_scheduler()

    yield

    stop_scheduler()
    await close_db()
    logger.info("Project Fifty shut down")


app = FastAPI(
    title="Project Fifty API",
    description=(
        "A 50-agent AI system for drought, heat, and climate monitoring in Rwanda. "
        "Agents collect satellite data, calculate drought severity indices, detect "
        "anomalies, and generate actionable intelligence for Cabinet briefings."
    ),
    version=settings.PROJECT_VERSION,
    contact={"name": "Project Fifty Team"},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    """Health ping endpoint."""
    return {
        "project": "Project Fifty",
        "status": "running",
        "version": settings.PROJECT_VERSION,
    }


@app.get("/health")
async def health():
    """Full health check."""
    from app.orchestration.registry import ALL_AGENTS
    from app.services.mistral import mistral_service

    db_status = "connected"
    try:
        from sqlalchemy import text
        from app.core.database import engine
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unavailable"

    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "database": db_status,
        "mistral_api_configured": mistral_service.validate_api_key(),
        "agents_registered": len(ALL_AGENTS),
    }
