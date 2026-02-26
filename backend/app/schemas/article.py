from datetime import datetime

from pydantic import BaseModel


class ArticleOut(BaseModel):
    id: int
    title: str
    canonical_url: str
    summary: str | None = None
    key_insights: list[str] | None = None
    category: str | None = None
    source: str
    country: str | None = None
    published_at: datetime | None = None
    company_tags: list[str] | None = None
    model_tags: list[str] | None = None
    topic_tags: list[str] | None = None
    is_breaking: bool = False


class DigestQuery(BaseModel):
    question: str
    days: int = 7
