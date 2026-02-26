from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import feedparser
import httpx
from dateutil import parser as date_parser

from app.core.config import get_settings


@dataclass
class RawArticle:
    title: str
    url: str
    content: str | None
    published_at: datetime | None
    source_name: str
    source_type: str
    country: str | None = None


class IngestionService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def fetch_all(self) -> list[RawArticle]:
        results: list[RawArticle] = []
        results.extend(await self.fetch_news_apis())
        results.extend(await self.fetch_rss_feeds())
        results.extend(await self.fetch_research())
        results.extend(await self.fetch_community())
        return results

    async def fetch_news_apis(self) -> list[RawArticle]:
        tasks = [
            self._fetch_newsapi(),
            self._fetch_newsdata(),
            self._fetch_gnews(),
        ]
        output: list[RawArticle] = []
        for task in tasks:
            try:
                output.extend(await task)
            except Exception:
                continue
        return output

    async def _fetch_newsapi(self) -> list[RawArticle]:
        if not self.settings.newsapi_key:
            return []
        params = {'q': 'artificial intelligence OR LLM OR AI startup', 'apiKey': self.settings.newsapi_key, 'language': 'en'}
        async with httpx.AsyncClient(timeout=20) as client:
            data = (await client.get('https://newsapi.org/v2/everything', params=params)).json()
        return [self._from_newsapi(item) for item in data.get('articles', [])]

    async def _fetch_newsdata(self) -> list[RawArticle]:
        if not self.settings.newsdata_key:
            return []
        params = {'apikey': self.settings.newsdata_key, 'q': 'artificial intelligence', 'language': 'en'}
        async with httpx.AsyncClient(timeout=20) as client:
            data = (await client.get('https://newsdata.io/api/1/news', params=params)).json()
        return [self._from_newsdata(item) for item in data.get('results', [])]

    async def _fetch_gnews(self) -> list[RawArticle]:
        if not self.settings.gnews_key:
            return []
        params = {'q': 'artificial intelligence', 'token': self.settings.gnews_key, 'lang': 'en'}
        async with httpx.AsyncClient(timeout=20) as client:
            data = (await client.get('https://gnews.io/api/v4/search', params=params)).json()
        return [self._from_gnews(item) for item in data.get('articles', [])]

    async def fetch_rss_feeds(self) -> list[RawArticle]:
        feeds = {
            'TechCrunch AI': 'https://techcrunch.com/tag/artificial-intelligence/feed/',
            'VentureBeat AI': 'https://venturebeat.com/category/ai/feed/',
            'MIT Tech Review': 'https://www.technologyreview.com/topic/artificial-intelligence/feed/',
            'OpenAI Blog': 'https://openai.com/news/rss.xml',
            'Google AI Blog': 'https://blog.google/technology/ai/rss/',
            'Meta AI Blog': 'https://ai.meta.com/blog/rss/',
        }
        output: list[RawArticle] = []
        for name, url in feeds.items():
            parsed = feedparser.parse(url)
            for entry in parsed.entries:
                output.append(
                    RawArticle(
                        title=entry.get('title', 'Untitled'),
                        url=entry.get('link'),
                        content=entry.get('summary'),
                        published_at=date_parser.parse(entry.published) if entry.get('published') else None,
                        source_name=name,
                        source_type='rss',
                    )
                )
        return output

    async def fetch_research(self) -> list[RawArticle]:
        async with httpx.AsyncClient(timeout=20) as client:
            arxiv = feedparser.parse('https://export.arxiv.org/rss/cs.AI')
            hf = (await client.get('https://huggingface.co/api/trending')).json()
        output = [
            RawArticle(
                title=e.get('title', 'Untitled'),
                url=e.get('link'),
                content=e.get('summary'),
                published_at=date_parser.parse(e.published) if e.get('published') else None,
                source_name='ArXiv cs.AI',
                source_type='research',
            )
            for e in arxiv.entries
        ]
        output.extend(
            RawArticle(
                title=item.get('title', 'HuggingFace Trend'),
                url=f"https://huggingface.co/{item.get('repoData', {}).get('id', '')}",
                content=item.get('description'),
                published_at=None,
                source_name='HuggingFace Trending',
                source_type='research',
            )
            for item in hf[:20]
            if isinstance(item, dict)
        )
        return output

    async def fetch_community(self) -> list[RawArticle]:
        urls = {
            'Hacker News': 'https://hn.algolia.com/api/v1/search?query=artificial+intelligence',
            'Reddit MachineLearning': 'https://www.reddit.com/r/MachineLearning/new.json?limit=25',
            'Reddit Artificial': 'https://www.reddit.com/r/artificial/new.json?limit=25',
        }
        output: list[RawArticle] = []
        headers = {'User-Agent': 'global-ai-intelligence-portal/1.0'}
        async with httpx.AsyncClient(timeout=20, headers=headers) as client:
            hn = (await client.get(urls['Hacker News'])).json()
            for hit in hn.get('hits', []):
                output.append(
                    RawArticle(
                        title=hit.get('title') or 'HN Story',
                        url=hit.get('url') or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                        content=hit.get('story_text'),
                        published_at=date_parser.parse(hit['created_at']) if hit.get('created_at') else None,
                        source_name='Hacker News',
                        source_type='community',
                    )
                )
            for source_name in ('Reddit MachineLearning', 'Reddit Artificial'):
                response = (await client.get(urls[source_name])).json()
                for child in response.get('data', {}).get('children', []):
                    data: dict[str, Any] = child.get('data', {})
                    output.append(
                        RawArticle(
                            title=data.get('title', 'Reddit Post'),
                            url=f"https://reddit.com{data.get('permalink', '')}",
                            content=data.get('selftext'),
                            published_at=datetime.utcfromtimestamp(data.get('created_utc', 0)) if data.get('created_utc') else None,
                            source_name=source_name,
                            source_type='community',
                        )
                    )
        return output

    def _from_newsapi(self, item: dict[str, Any]) -> RawArticle:
        return RawArticle(
            title=item.get('title', 'Untitled'),
            url=item.get('url'),
            content=item.get('content'),
            published_at=date_parser.parse(item['publishedAt']) if item.get('publishedAt') else None,
            source_name='NewsAPI',
            source_type='api',
        )

    def _from_newsdata(self, item: dict[str, Any]) -> RawArticle:
        return RawArticle(
            title=item.get('title', 'Untitled'),
            url=item.get('link'),
            content=item.get('description'),
            published_at=date_parser.parse(item['pubDate']) if item.get('pubDate') else None,
            source_name='NewsData.io',
            source_type='api',
            country=(item.get('country') or [None])[0],
        )

    def _from_gnews(self, item: dict[str, Any]) -> RawArticle:
        return RawArticle(
            title=item.get('title', 'Untitled'),
            url=item.get('url'),
            content=item.get('description'),
            published_at=date_parser.parse(item['publishedAt']) if item.get('publishedAt') else None,
            source_name='GNews',
            source_type='api',
        )
