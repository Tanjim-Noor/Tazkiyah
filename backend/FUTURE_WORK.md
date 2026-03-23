# Backend Future Work

This backend folder now contains the first implementation slice of the FastAPI + LangGraph API.

## Implemented

- FastAPI application scaffold with lifespan startup in `backend/main.py`
- Endpoint set:
	- `GET /health`
	- `GET /api/v1/config`
	- `POST /api/v1/chat` (SSE)
- LangGraph orchestration pipeline in `backend/graph/`
	- LLM-only classification
	- Fixed category routing
	- Category-specific prompt engineering
	- Retrieval and final prompt assembly
- Provider-agnostic adapter interfaces in `backend/adapters/interfaces.py`
- Default provider adapters:
	- Ollama (`backend/adapters/ollama_langchain.py`)
	- Chroma (`backend/adapters/chroma_langchain.py`)
- LangSmith tracing wiring via backend settings
- Integration tests in `backend/tests/test_api.py`

## Current Category Set

- Factual & Informational
- Emotional & Empathetic
- Creative

## Next Phases

- Add indexing and readiness operations as explicit backend service endpoints.
- Add stronger retrieval controls (score thresholds, optional reranking).
- Add chat history/session persistence.
- Add auth strategy when frontend integration is stabilized.
- Add production hardening (timeouts, retries, observability metrics, rate limiting).

## Boundaries

- Existing `tools/python/rag_v2` remains unchanged and is treated as reference only.
- Backend orchestration and API concerns stay isolated under `backend/`.