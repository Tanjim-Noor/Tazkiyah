# Tazkiyah Backend (FastAPI + LangGraph)

This backend provides API endpoints for the Quran chatbot using LangGraph orchestration.

## Implemented Scope (Phase 1)

- FastAPI app with lifespan startup.
- LangGraph orchestration for:
  - Query classification (LLM-only)
  - Category-specific prompt engineering
  - Retrieval from Chroma vector store
  - Final prompt construction for generation
- SSE chat streaming endpoint for frontend integration.
- Runtime config endpoint.
- Health endpoint.
- LangSmith tracing integration.

## Fixed Query Categories

- Factual & Informational
- Emotional & Empathetic
- Creative

## API Endpoints

- `GET /health`
- `GET /api/v1/config`
- `POST /api/v1/chat` (SSE stream)

## Run

From repository root:

```powershell
& "d:/Work/Quran Project/Tazkiyah/venv/Scripts/python.exe" -m uvicorn backend.main:app --reload
```

Open docs:

- `http://127.0.0.1:8000/docs`

## SSE Chat Request Example

```powershell
curl -N -X POST "http://127.0.0.1:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What does Surah Al-Fatihah teach us?\",\"return_sources\":true}"
```

The stream emits events:

- `meta`
- `token`
- `done`
- `error`

## Testing

```powershell
& "d:/Work/Quran Project/Tazkiyah/venv/Scripts/python.exe" -m pytest backend/tests -q
```

## Design Notes

- Existing `tools/python/rag_v2` remains untouched and serves as reference.
- Backend uses adapter interfaces for provider/model/vector-store agnostic architecture.
- Current provider defaults are Ollama + Chroma with env-driven settings.
