from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.workers.scheduler import start_scheduler

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.on_event('startup')
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    start_scheduler()


@app.get('/healthz')
def health() -> dict[str, str]:
    return {'status': 'ok'}
