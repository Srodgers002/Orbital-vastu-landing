from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Source(Base):
    __tablename__ = 'sources'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    source_type: Mapped[str] = mapped_column(String(30))  # api, rss, research, community
    url: Mapped[str] = mapped_column(String(500))
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)


class Article(Base):
    __tablename__ = 'articles'
    __table_args__ = (UniqueConstraint('canonical_url', name='uq_articles_canonical_url'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(400), index=True)
    canonical_url: Mapped[str] = mapped_column(String(600), index=True)
    raw_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    key_insights: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'))
    source_id: Mapped[int] = mapped_column(ForeignKey('sources.id'))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    company_tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    model_tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    topic_tags: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    is_breaking: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    source: Mapped['Source'] = relationship()
    category: Mapped['Category'] = relationship()


class Embedding(Base):
    __tablename__ = 'embeddings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey('articles.id'), unique=True)
    vector_id: Mapped[str] = mapped_column(String(120), unique=True)
    model_name: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    __table_args__ = (UniqueConstraint('user_id', 'article_id', name='uq_user_article_bookmark'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    article_id: Mapped[int] = mapped_column(ForeignKey('articles.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
