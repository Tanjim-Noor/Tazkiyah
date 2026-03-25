from __future__ import annotations

import json

from fastapi.testclient import TestClient

from backend.api.deps import get_quran_api_testing_service, get_rag_service
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
    def answer(self, *, query, top_k, temperature, return_sources):
        # Reuse stream behavior for fake service in sync mode.
        final_answer = ""
        category = "Factual & Informational"
        sources = [
            {
                "verse_id": "1:1",
                "surah_name": "Al-Fatihah",
                "surah_number": 1,
                "verse_number": 1,
                "score": 0.1,
            }
        ] if return_sources else []
        return {"answer": "Assalamu alaykum", "category": category, "sources": sources}


class FakeQuranAPITestingService:
    def resources(self, language: str | None):
        _ = language
        return {
            "language": "en",
            "translations": [
                {
                    "id": 20,
                    "name": "Saheeh International",
                    "language_name": "english",
                    "author_name": "Saheeh",
                }
            ],
            "tafsirs": [
                {
                    "id": 169,
                    "name": "Tafsir Ibn Kathir",
                    "language_name": "english",
                    "author_name": "Ibn Kathir",
                }
            ],
        }

    def verse_details(self, payload):
        _ = payload
        return {
            "verse_key": "13:28",
            "requested_include": ["arabic", "translations", "metadata"],
            "warnings": [],
            "duration_ms": 25,
            "data": {
                "arabic_text": "الذين آمنوا وتطمئن قلوبهم بذكر الله",
                "transliteration": None,
                "translations": [
                    {
                        "id": 20,
                        "name": "Saheeh International",
                        "language_name": "english",
                        "text": "Those who have believed and whose hearts are assured by the remembrance of Allah.",
                    }
                ],
                "tafsirs": [],
                "footnotes": [],
                "metadata": {
                    "surah_number": 13,
                    "verse_number": 28,
                    "surah_name": "Ar-Ra'd",
                    "surah_name_arabic": "الرعد",
                    "juz": 13,
                    "page": 252,
                    "hizb": 26,
                    "rub_el_hizb": 52,
                    "ruku": 2,
                    "manzil": 3,
                    "sajdah": None,
                    "revelation_place": "madinah",
                    "revelation_order": 96,
                },
                "raw": None,
            },
        }

def _test_client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_rag_service] = lambda: FakeRAGService()
    app.dependency_overrides[get_quran_api_testing_service] = lambda: FakeQuranAPITestingService()
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


def test_chat_sync_endpoint():
    client = _test_client()
    response = client.post(
        "/api/v1/chat/sync",
        json={
            "query": "What does surah fatiha mean?",
            "top_k": 1,
            "temperature": 0.5,
            "return_sources": True,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "Factual & Informational"
    assert body["answer"] == "Assalamu alaykum"
    assert isinstance(body["sources"], list)


def test_quran_resources_endpoint():
    client = _test_client()
    response = client.get("/api/v1/quran-testing/resources?language=en")

    assert response.status_code == 200
    payload = response.json()
    assert payload["language"] == "en"
    assert payload["translations"][0]["id"] == 20
    assert payload["tafsirs"][0]["id"] == 169


def test_quran_verse_endpoint():
    client = _test_client()
    response = client.post(
        "/api/v1/quran-testing/verse",
        json={
            "verse_key": "13:28",
            "include": ["arabic", "translations", "metadata"],
            "translation_ids": [20],
            "tafsir_ids": [],
            "language": "en",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["verse_key"] == "13:28"
    assert payload["data"]["arabic_text"]
    assert payload["data"]["translations"][0]["id"] == 20

