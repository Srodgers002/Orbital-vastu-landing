import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models.entities import Article
from app.services.ingestion import IngestionService
from app.services.pipeline import AIPipeline

scheduler = BackgroundScheduler()


def run_ingestion_job() -> None:
    asyncio.run(_ingest())


async def _ingest() -> None:
    service = IngestionService()
    batch = await service.fetch_all()
    db: Session = SessionLocal()
    try:
        pipeline = AIPipeline(db)
        pipeline.ingest_batch(batch)
    finally:
        db.close()


def rebuild_embeddings_job() -> None:
    db: Session = SessionLocal()
    try:
        pipeline = AIPipeline(db)
        for article in db.scalars(select(Article)).all():
            pipeline.embed_article(article)
        db.commit()
    finally:
        db.close()


def start_scheduler() -> None:
    settings = get_settings()
    scheduler.add_job(run_ingestion_job, 'interval', minutes=settings.fetch_interval_minutes, id='fetch-news')
    scheduler.add_job(rebuild_embeddings_job, 'cron', hour=3, minute=0, id='rebuild-embeddings')
    scheduler.start()
