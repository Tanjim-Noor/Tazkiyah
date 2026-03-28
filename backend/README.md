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
- Model-specific Chroma vector store resolution based on the active embedding model.

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

## Vector Store Builds

The backend resolves the Chroma persist path from the embedding model when `CHROMA_PERSIST_DIR` is not set. The resolved path is exposed from `GET /api/v1/config` so you can see which store is active.

List the stores that already exist before switching models:

```powershell
python -m tools.python.rag_v2.list_vectorstores
```

Build a store with the matching model using:

```powershell
python -m tools.python.rag_v2.build_vectorstore --embedding-model "nomic-embed-text-v2-moe"
```

The resulting directory looks like:

```text
data/vectorstores/rag_v2/ollama/nomic-embed-text-v2-moe/quran_tazkiyah_v2
```

When you switch models, build the target store once and then reuse it. If the model needs custom query or document prefixes, keep that logic in the pipeline and record the rule in [docs/embedding-model-switching.md](../docs/embedding-model-switching.md).

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
