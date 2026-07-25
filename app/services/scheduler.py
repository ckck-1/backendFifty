"""Daily pipeline scheduler — triggers agent pipeline at 06:00 RST."""
from __future__ import annotations

import logging
from datetime import datetime

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

RST = pytz.timezone("Africa/Kigali")

scheduler = AsyncIOScheduler(timezone=RST)


async def daily_pipeline_job() -> None:
    """Run the full agent pipeline for all 416 sectors."""
    from app.orchestration.orchestrator import orchestrator
    from app.core.database import async_session

    logger.info("Daily pipeline triggered at %s RST", datetime.now(RST).isoformat())

    default_sectors = [
        "Bugesera", "Nyagatare", "Huye", "Musanze", "Rubavu",
    ]

    async with async_session() as db:
        for sector in default_sectors:
            try:
                await orchestrator.run(
                    location=sector,
                    query="Full drought and heat analysis for daily monitoring",
                    db=db,
                )
                logger.info("Completed analysis for %s", sector)
            except Exception as exc:
                logger.error("Pipeline failed for %s: %s", sector, exc)

    logger.info("Daily pipeline finished")


def start_scheduler() -> None:
    """Add jobs and start the scheduler."""
    scheduler.add_job(
        daily_pipeline_job,
        CronTrigger(hour=6, minute=0),
        id="daily_pipeline",
        name="Daily Climate Pipeline (06:00 RST)",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started — daily pipeline at 06:00 RST")


def stop_scheduler() -> None:
    """Shut down the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
