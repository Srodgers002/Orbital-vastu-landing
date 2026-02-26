from __future__ import annotations

import hashlib
import json
from collections import Counter

from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.entities import Article, Category, Embedding, Source
from app.services.ingestion import RawArticle
from app.services.vector_store import VectorStore


class AIPipeline:
    categories = ['Research', 'Startup', 'Product Launch', 'Regulation', 'Funding', 'Ethics']

    def __init__(self, db: Session):
        self.db = db
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.settings = settings
        self.vector_store = VectorStore(settings.chroma_persist_dir, settings.embedding_model)

    def ingest_batch(self, raw_articles: list[RawArticle]) -> int:
        inserted = 0
        for raw in raw_articles:
            if not raw.url:
                continue
            canonical_url = raw.url.split('?')[0]
            exists = self.db.scalar(select(Article.id).where(Article.canonical_url == canonical_url))
            if exists:
                continue
            source = self._get_or_create_source(raw)
            category_name = self.classify(raw)
            category = self._get_or_create_category(category_name)
            summary, insights = self.summarize(raw)
            article = Article(
                title=raw.title[:390],
                canonical_url=canonical_url,
                raw_content=raw.content,
                summary=summary,
                key_insights=insights,
                category_id=category.id,
                source_id=source.id,
                published_at=raw.published_at,
                country=raw.country,
                company_tags=self.extract_tags(raw.title, 'company'),
                model_tags=self.extract_tags(raw.title, 'model'),
                topic_tags=self.extract_tags(raw.title, 'topic'),
            )
            self.db.add(article)
            self.db.flush()
            self.embed_article(article)
            inserted += 1
        self.db.commit()
        return inserted

    def classify(self, raw: RawArticle) -> str:
        if not self.client:
            title = raw.title.lower()
            if 'funding' in title or 'raises' in title:
                return 'Funding'
            if 'regulation' in title or 'policy' in title:
                return 'Regulation'
            return 'Research'
        prompt = f"Classify this AI news title into one category {self.categories}: {raw.title}"
        resp = self.client.responses.create(model=self.settings.openai_model, input=prompt)
        category = resp.output_text.strip()
        return category if category in self.categories else 'Research'

    def summarize(self, raw: RawArticle) -> tuple[str, list[str]]:
        content = (raw.content or raw.title)[:3000]
        if not self.client:
            return (f"{raw.title}. Source: {raw.source_name}.", ['Monitor for updates', 'Auto summary fallback'])
        prompt = (
            'Summarize this AI news in exactly 2 lines and then 5 concise bullet insights as JSON '
            '{"summary":"...","insights":["..."]}. Content: '
            + content
        )
        resp = self.client.responses.create(model=self.settings.openai_model, input=prompt)
        try:
            parsed = json.loads(resp.output_text)
            return parsed['summary'], parsed['insights'][:5]
        except Exception:
            return resp.output_text[:250], ['AI parse fallback']

    def embed_article(self, article: Article) -> None:
        text = ' '.join(filter(None, [article.title, article.summary, article.raw_content]))[:5000]
        vector_id = hashlib.sha1(article.canonical_url.encode()).hexdigest()
        embedding = self.vector_store.embed_and_upsert(vector_id, text, {'article_id': article.id})
        self.db.add(Embedding(article_id=article.id, vector_id=vector_id, model_name=embedding['model']))

    def detect_trends(self) -> list[dict[str, int]]:
        rows = self.db.execute(select(Article.topic_tags).where(Article.topic_tags.is_not(None))).all()
        counter = Counter(tag for (tags,) in rows for tag in (tags or []))
        return [{'topic': topic, 'count': count} for topic, count in counter.most_common(10)]

    def _get_or_create_source(self, raw: RawArticle) -> Source:
        source = self.db.scalar(select(Source).where(Source.name == raw.source_name))
        if source:
            return source
        source = Source(name=raw.source_name, source_type=raw.source_type, url=raw.url)
        self.db.add(source)
        self.db.flush()
        return source

    def _get_or_create_category(self, name: str) -> Category:
        category = self.db.scalar(select(Category).where(Category.name == name))
        if category:
            return category
        category = Category(name=name)
        self.db.add(category)
        self.db.flush()
        return category

    def extract_tags(self, text: str, tag_type: str) -> list[str]:
        tokens = [t.strip(',.') for t in text.split() if len(t) > 3]
        if tag_type == 'company':
            return [t for t in tokens if t[0].isupper()][:3]
        if tag_type == 'model':
            return [t for t in tokens if t.lower().startswith(('gpt', 'llama', 'claude', 'gemini'))][:3]
        return list({t.lower() for t in tokens[:5]})
