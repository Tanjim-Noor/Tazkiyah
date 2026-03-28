# Tazkiyah Backend API Documentation

This document describes all backend APIs currently implemented in the FastAPI service.

- Service title: Tazkiyah Backend
- Default local base URL: http://127.0.0.1:8000
- API prefix for feature routes: /api/v1
- Content types used:
  - application/json
  - text/event-stream (SSE)

## 1) Authentication

No authentication is currently required for these endpoints.

## 2) CORS

CORS is enabled with settings from backend/config.py:

- allow_origins: ["*"] by default
- allow_credentials: true
- allow_methods: ["*"]
- allow_headers: ["*"]

This allows frontend development from any origin by default.

## 3) Error Model (FastAPI Standard)

For request validation errors, FastAPI returns status 422 with this shape:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "validation error message",
      "type": "error_type"
    }
  ]
}
```

For streaming endpoint runtime errors, the endpoint emits an SSE event named error instead of returning a JSON error body.

## 4) Endpoint Summary

- GET /health
- GET /api/v1/config
- POST /api/v1/chat (SSE streaming)
- POST /api/v1/chat/sync (JSON, non-streaming)

---

## 5) GET /health

Health check for vector store and LLM readiness.

### Request

- Method: GET
- URL: /health
- Body: none

### Response

- Status: 200
- Content-Type: application/json

Schema:

```json
{
  "status": "ok | degraded",
  "service": "tazkiyah-backend",
  "vectorstore_ready": true,
  "llm_ready": true
}
```

Example:

```json
{
  "status": "ok",
  "service": "tazkiyah-backend",
  "vectorstore_ready": true,
  "llm_ready": true
}
```

---

## 6) GET /api/v1/config

Returns runtime configuration useful for frontend behavior and diagnostics.

### Request

- Method: GET
- URL: /api/v1/config
- Body: none

### Response

- Status: 200
- Content-Type: application/json

Schema:

```json
{
  "app_name": "Tazkiyah Backend",
  "environment": "development",
  "llm_provider": "ollama",
  "embedding_provider": "ollama",
  "vectorstore_provider": "chroma",
  "llm_model": "qwen3.5:9b",
  "embedding_model": "jina/jina-embeddings-v2-base-en",
  "chroma_persist_dir": "d:/work/quran project/tazkiyah/data/vectorstores/rag_v2/ollama/jina-embeddings-v2-base-en/quran_tazkiyah_v2",
  "collection_name": "quran_tazkiyah_v2",
  "top_k": 5,
  "categories": [
    "Factual & Informational",
    "Emotional & Empathetic",
    "Creative"
  ],
  "langsmith_tracing": true,
  "langsmith_project": "tazkiyah-rag-v2",
  "vector_count": 6102
}
```

Field notes:

- vector_count is critical for retrieval sanity.
- If vector_count is 0, chat answers may be low quality or empty-context.

---

## 7) POST /api/v1/chat (Streaming SSE)

Primary chat endpoint for real-time token streaming.

### Request

- Method: POST
- URL: /api/v1/chat
- Content-Type: application/json

Body schema:

```json
{
  "query": "string, required, min length 1",
  "top_k": "integer, optional, range 1..20",
  "temperature": "number, optional, range 0.0..2.0",
  "return_sources": "boolean, optional, default true"
}
```

Example request:

```json
{
  "query": "What does Surah Al-Fatihah teach us?",
  "top_k": 5,
  "temperature": 0.3,
  "return_sources": true
}
```

### Response

- Status: 200
- Content-Type: text/event-stream; charset=utf-8
- Transfer-Encoding: chunked

The stream emits events in this order:

1. meta
2. token (repeated 0..n times)
3. done

On exception, emits:

- error

### SSE Event Payloads

meta:

```text
event: meta
data: {"category":"Factual & Informational"}
```

token:

```text
event: token
data: {"text":"partial text chunk"}
```

done:

```text
event: done
data: {
  "answer":"final full answer",
  "category":"Factual & Informational",
  "sources":[
    {
      "verse_id":"2:255",
      "surah_name":"Al-Baqarah",
      "surah_number":2,
      "verse_number":255,
      "score":0.1234
    }
  ]
}
```

error:

```text
event: error
data: {"message":"error details"}
```

### Frontend Integration Notes

- Swagger UI does not reliably display SSE token streams.
- Use a custom SSE parser in frontend for this endpoint.
- If your client cannot consume SSE, use POST /api/v1/chat/sync.

---

## 8) POST /api/v1/chat/sync (Non-Streaming)

Frontend-friendly JSON chat endpoint (recommended for Swagger and simple REST clients).

### Request

- Method: POST
- URL: /api/v1/chat/sync
- Content-Type: application/json

Body schema is exactly the same as POST /api/v1/chat.

Example request:

```json
{
  "query": "What does Surah Al-Fatihah teach us?",
  "top_k": 5,
  "temperature": 0.3,
  "return_sources": true
}
```

### Response

- Status: 200
- Content-Type: application/json

Schema:

```json
{
  "answer": "string",
  "category": "Factual & Informational | Emotional & Empathetic | Creative",
  "sources": [
    {
      "verse_id": "string",
      "surah_name": "string | null",
      "surah_number": "number | null",
      "verse_number": "number | null",
      "score": "number | null"
    }
  ]
}
```

Example response:

```json
{
  "answer": "Surah Al-Fatihah teaches worship, guidance, and dependence on Allah...",
  "category": "Factual & Informational",
  "sources": [
    {
      "verse_id": "1:5",
      "surah_name": "Al-Fatihah",
      "surah_number": 1,
      "verse_number": 5,
      "score": 0.0842
    }
  ]
}
```

### Validation Errors

- Status: 422
- Returned when:
  - query is missing or empty
  - top_k is outside 1..20
  - temperature is outside 0.0..2.0

---

## 9) Frontend Implementation Guidance

## Recommended strategy

- Use /api/v1/chat/sync for initial frontend build, forms, and state wiring.
- Add /api/v1/chat streaming mode later for live token UX.

## Suggested UI behavior

- On app load:
  - call GET /health
  - call GET /api/v1/config
- Before chat send:
  - ensure query is non-empty
  - optionally clamp top_k and temperature client-side
- After response:
  - render answer markdown/text
  - render sources list with verse metadata

## Reliability checks

- If /api/v1/config returns vector_count = 0, display warning in UI.
- If chat returns empty sources, show "No retrieved source passages" state.
- If SSE used, handle event: error explicitly.

---

## 10) Copy-Paste Request Examples

## Health

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

## Config

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/config"
```

## Chat Sync

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/chat/sync" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does Surah Al-Fatihah teach us?",
    "top_k": 5,
    "temperature": 0.3,
    "return_sources": true
  }'
```

## Chat Stream (SSE)

```bash
curl -N -X POST "http://127.0.0.1:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does Surah Al-Fatihah teach us?",
    "top_k": 5,
    "temperature": 0.3,
    "return_sources": true
  }'
```

---

## 11) Current Limits and Notes

- top_k max is 20 by validation.
- temperature range is 0.0 to 2.0 by validation.
- /chat is SSE, not WebSocket.
- category is generated internally by the orchestration graph and returned in responses.
