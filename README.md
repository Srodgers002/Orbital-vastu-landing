# Global AI Intelligence Portal

Production-ready AI news intelligence platform focused exclusively on artificial intelligence developments.

## 1) Architecture Decision

- **Frontend**: Next.js App Router + TailwindCSS + TypeScript for modern UX, SEO, and rapid iteration.
- **Backend**: FastAPI chosen over Node because Python has stronger AI/data tooling for ingestion, summarization, and embeddings.
- **Datastores**:
  - PostgreSQL for durable relational data (articles, users, bookmarks, sources, categories).
  - Redis for caching and hot-feed acceleration.
  - ChromaDB for semantic search vectors and trend clustering.
- **AI Layer**: OpenAI API by default with deterministic fallback logic if keys are unavailable.
- **Automation**: APScheduler jobs every 15 minutes for ingestion; daily embedding rebuild.
- **Deployment**: Docker Compose for local prod-like orchestration + GitHub Actions CI.

## 2) Folder Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/routes.py
│   │   ├── core/config.py
│   │   ├── db/{base.py,session.py}
│   │   ├── models/entities.py
│   │   ├── schemas/article.py
│   │   ├── services/
│   │   │   ├── assistant.py
│   │   │   ├── ingestion.py
│   │   │   ├── notifications.py
│   │   │   ├── pipeline.py
│   │   │   ├── scraper.py
│   │   │   └── vector_store.py
│   │   ├── workers/scheduler.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/{page.tsx,search/page.tsx,assistant/page.tsx,layout.tsx,globals.css}
│   ├── components/{header.tsx,news-card.tsx}
│   ├── lib/api.ts
│   ├── Dockerfile
│   └── package.json
├── infra/schema.sql
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## 3) Backend APIs

- `GET /healthz`
- `GET /v1/articles` with filters: `country`, `company`, `ai_model`, `topic`
- `GET /v1/trending`
- `GET /v1/search?q=` semantic/text search entrypoint
- `POST /v1/assistant/digest` body `{ question, days }`
- `POST /v1/bookmarks/{article_id}`

## 4) Autonomous AI Agent Pipeline

1. **Agent 1 Fetcher** (`IngestionService`): pulls APIs + RSS + ArXiv + HuggingFace + Reddit + HN every 15 min.
2. **Agent 2 Deduplicator** (`AIPipeline.ingest_batch`): canonical URL unique checks.
3. **Agent 3 Classifier** (`AIPipeline.classify`): categories = Research/Startup/Product Launch/Regulation/Funding/Ethics.
4. **Agent 4 Summarizer** (`AIPipeline.summarize`): 2-line summary + 5 insights.
5. **Agent 5 Trend Detector** (`AIPipeline.detect_trends`): tag-frequency + embedding storage for clustering workflows.

Fallback scraping exists with Playwright (`services/scraper.py`) when sources fail.

## 5) Frontend Features Implemented

- Homepage with trending alerts and latest AI coverage.
- Semantic Search page.
- Ask AI Assistant digest page ("What happened in AI this week?").
- Futuristic dark glassmorphism UI.
- Mobile-first responsive layout.

## 6) Database Schema

Defined in `infra/schema.sql` and mirrored in SQLAlchemy models:

- `articles`
- `sources`
- `categories`
- `embeddings`
- `users`
- `bookmarks`

## 7) Installation & Run

### Prerequisites
- Docker + Docker Compose

### Start
```bash
docker compose up --build
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8000/docs`

## 8) CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`) runs:
- Python dependency install + compile check
- Next.js install + production build

## 9) Bonus Integrations (Optional)

- **Email newsletter**: `services/notifications.py::send_newsletter`
- **Telegram alert bot**: `services/notifications.py::send_telegram_alert`

Wire these to scheduler jobs or event hooks for breaking news pushes.
