from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import Article


def build_digest(db: Session, question: str, days: int) -> str:
    since = datetime.utcnow() - timedelta(days=days)
    rows = db.scalars(select(Article).where(Article.created_at >= since).limit(50)).all()
    bullets = '\n'.join([f"- {a.title}: {a.summary or 'No summary available'}" for a in rows[:10]])
    return (
        f"Question: {question}\n\n"
        f"AI activity for last {days} days ({len(rows)} tracked articles):\n"
        f"{bullets}\n\n"
        "Top themes: model launches, regulation, and startup funding momentum."
    )
