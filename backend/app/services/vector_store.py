from __future__ import annotations

import chromadb

from app.core.config import get_settings


class VectorStore:
    def __init__(self, persist_dir: str, embedding_model: str):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection('ai_news_embeddings')
        self.embedding_model = embedding_model
        self.settings = get_settings()

    def embed_and_upsert(self, vector_id: str, text: str, metadata: dict) -> dict:
        # Chroma can auto-embed when no explicit embedding function is passed.
        self.collection.upsert(ids=[vector_id], documents=[text], metadatas=[metadata])
        return {'id': vector_id, 'model': self.embedding_model}

    def semantic_search(self, query: str, top_k: int = 10) -> list[str]:
        resp = self.collection.query(query_texts=[query], n_results=top_k)
        ids = resp.get('ids', [[]])[0]
        return ids
