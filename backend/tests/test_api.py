from __future__ import annotations

import json

from fastapi.testclient import TestClient

from backend.api.deps import get_rag_service
from backend.main import create_app


class FakeRAGService:
    def health(self):
        return {
            "status": "ok",
            "service": "tazkiyah-backend",
            "vectorstore_ready": True,
            "llm_ready": True,
        }

    def runtime_config(self):
        return {
            "app_name": "Tazkiyah Backend",
            "environment": "test",
            "llm_provider": "ollama",
            "embedding_provider": "ollama",
            "vectorstore_provider": "chroma",
            "llm_model": "test-llm",
            "embedding_model": "test-embed",
            "collection_name": "test-collection",
            "top_k": 5,
            "categories": [
                "Factual & Informational",
                "Emotional & Empathetic",
                "Creative",
            ],
            "langsmith_tracing": True,
            "langsmith_project": "test-project",
            "vector_count": 10,
        }

    async def stream_answer(self, *, query, top_k, temperature, return_sources):
        _ = (query, top_k, temperature, return_sources)
        yield {"event": "meta", "data": {"category": "Factual & Informational"}}
        yield {"event": "token", "data": {"text": "Assalamu "}}
        yield {"event": "token", "data": {"text": "alaykum"}}
        yield {
            "event": "done",
            "data": {
                "answer": "Assalamu alaykum",
                "category": "Factual & Informational",
                "sources": [
                    {
                        "verse_id": "1:1",
                        "surah_name": "Al-Fatihah",
                        "surah_number": 1,
                        "verse_number": 1,
                        "score": 0.1,
                    }
                ],
            },
        }

    @staticmethod
    def format_sse(event: str, payload: dict) -> str:
        return f"event: {event}\\ndata: {json.dumps(payload)}\\n\\n"


def _test_client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_rag_service] = lambda: FakeRAGService()
    return TestClient(app)


def test_health_endpoint():
    client = _test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_config_endpoint():
    client = _test_client()
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    body = response.json()
    assert body["llm_model"] == "test-llm"
    assert body["vector_count"] == 10


def test_chat_sse_endpoint():
    client = _test_client()
    with client.stream(
        "POST",
        "/api/v1/chat",
        json={"query": "What does surah fatiha mean?"},
    ) as response:
        assert response.status_code == 200
        text = "".join(response.iter_text())

    assert "event: meta" in text
    assert "event: token" in text
    assert "event: done" in text
