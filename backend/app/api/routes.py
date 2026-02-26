from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.entities import Article, Bookmark, Category, Source
from app.schemas.article import ArticleOut, DigestQuery
from app.services.assistant import build_digest
from app.services.vector_store import VectorStore
from app.core.config import get_settings

router = APIRouter(prefix='/v1')


def _to_article_out(row: Article) -> ArticleOut:
    return ArticleOut(
        id=row.id,
        title=row.title,
        canonical_url=row.canonical_url,
        summary=row.summary,
        key_insights=row.key_insights,
        category=row.category.name if row.category else None,
        source=row.source.name if row.source else 'Unknown',
        country=row.country,
        published_at=row.published_at,
        company_tags=row.company_tags,
        model_tags=row.model_tags,
        topic_tags=row.topic_tags,
        is_breaking=row.is_breaking,
    )


@router.get('/articles', response_model=list[ArticleOut])
def list_articles(
    country: str | None = None,
    company: str | None = None,
    model: str | None = Query(default=None, alias='ai_model'),
    topic: str | None = None,
    db: Session = Depends(get_db),
):
    query = select(Article).join(Source).join(Category, isouter=True).order_by(desc(Article.published_at)).limit(100)
    if country:
        query = query.where(Article.country == country)
    rows = db.scalars(query).all()
    filtered = []
    for row in rows:
        if company and company not in (row.company_tags or []):
            continue
        if model and model not in (row.model_tags or []):
            continue
        if topic and topic not in (row.topic_tags or []):
            continue
        filtered.append(_to_article_out(row))
    return filtered


@router.get('/trending')
def trending(db: Session = Depends(get_db)):
    rows = db.scalars(select(Article).where(Article.is_breaking.is_(True)).order_by(desc(Article.created_at)).limit(20)).all()
    return [_to_article_out(row) for row in rows]


@router.get('/search', response_model=list[ArticleOut])
def semantic_search(q: str, db: Session = Depends(get_db)):
    settings = get_settings()
    _ = VectorStore(settings.chroma_persist_dir, settings.embedding_model).semantic_search(q)
    # vector ids are hashed URLs; fallback textual search for demo
    rows = db.scalars(select(Article).where(Article.title.ilike(f'%{q}%')).limit(20)).all()
    return [_to_article_out(row) for row in rows]


@router.post('/assistant/digest')
def digest(payload: DigestQuery, db: Session = Depends(get_db)):
    return {'answer': build_digest(db, payload.question, payload.days)}


@router.post('/bookmarks/{article_id}')
def add_bookmark(article_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    bookmark = Bookmark(user_id=user_id, article_id=article_id)
    db.add(bookmark)
    db.commit()
    return {'status': 'ok'}
