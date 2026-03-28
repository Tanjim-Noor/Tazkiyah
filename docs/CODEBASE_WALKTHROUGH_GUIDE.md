# Tazkiyah Codebase Walkthrough Guide

Audience: mixed (technical + non-technical)
Goal: explain what each part does, why it exists, and how data flows end-to-end.

## 1) 60-Second Big Picture

Non-technical version:
Tazkiyah is a Quranic guidance assistant. A user asks a question in natural language, and the system finds relevant Quranic context and returns a grounded answer with references.

Technical version:
Tazkiyah is a Retrieval-Augmented Generation (RAG) system built with FastAPI, LangGraph orchestration, Ollama-based model adapters, and a Chroma vector store.

## 2) Repository Map (What to Open During Demo)

### backend/

Non-technical:
This is the "engine room" where requests are processed and answers are generated.

Technical:
FastAPI app, route handlers, orchestration graph, service layer, adapters, and schemas.

Open in this order:
1. [backend/main.py](../backend/main.py)
2. [backend/api/routes/chat.py](../backend/api/routes/chat.py)
3. [backend/services/rag_service.py](../backend/services/rag_service.py)
4. [backend/graph/workflow.py](../backend/graph/workflow.py)
5. [backend/api/routes/configuration.py](../backend/api/routes/configuration.py)

### data/

Non-technical:
This stores Quran-related source data and prepared files used by the AI system.

Technical:
Raw/processed datasets and sample chunked artifacts for ingestion and testing.

### docs/

Non-technical:
Project manuals for setup, architecture, and engineering decisions.

Technical:
Operational and architectural references, including model-switching workflow.

Most useful during presentation:
1. docs/PROJECT_PRESENTATION_SCRIPT.md
2. docs/embedding-model-switching.md
3. docs/REPOSITORY_STRUCTURE.md

### tools/python/rag_v2/

Non-technical:
Utility tools to build and inspect the knowledge index behind answers.

Technical:
CLI scripts for indexing, vectorstore pathing, retrieval testing, and model-specific build workflows.

## 3) End-to-End Request Flow

1. User sends a query to POST /api/v1/chat or /api/v1/chat/sync.
2. Route calls RAGService.
3. RAGService runs graph workflow:
   - classify query type
   - retrieve relevant context from Chroma
   - assemble final prompt
   - call chat model
4. Response is returned with optional source references.
5. For streaming, SSE emits: meta -> sources -> token(s) -> done.

## 4) Explaining Key Files Two Ways

### [backend/main.py](../backend/main.py)

Plain language:
Starts the app and wires everything together at launch.

Technical:
Defines FastAPI lifespan startup, initializes service instances, and registers API routers.

### [backend/api/routes/chat.py](../backend/api/routes/chat.py)

Plain language:
This is the endpoint users talk to.

Technical:
Implements streaming and non-streaming chat endpoints, request validation, and service delegation.

### [backend/services/rag_service.py](../backend/services/rag_service.py)

Plain language:
The core brain that fetches relevant Quran context and builds responses.

Technical:
Coordinates adapter calls (embedding/chat/vectorstore), retrieval, prompt assembly, output sanitization, and source packaging.

### [backend/graph/workflow.py](../backend/graph/workflow.py)

Plain language:
A decision path that ensures each question is handled in the right order.

Technical:
LangGraph node/edge orchestration for classification, retrieval, and prompt finalization.

### [tools/python/rag_v2/build_vectorstore.py](../tools/python/rag_v2/build_vectorstore.py)

Plain language:
Creates the searchable Quran knowledge index.

Technical:
Builds model-specific vectorstore data for retrieval using selected embedding configuration.

## 5) Live Demo Storyline (Code + Product)

1. Show /health and /api/v1/config.
2. Run /api/v1/chat/sync and show sources.
3. Run /api/v1/chat stream and highlight event sequence.
4. Open backend/main.py and backend/api/routes/chat.py.
5. Open backend/services/rag_service.py and backend/graph/workflow.py.
6. Show tools/python/rag_v2/list_vectorstores.py and explain model isolation.

## 6) Common Audience Questions

Q: Is this just a generic chatbot?
A: No. It is grounded in Quran-specific retrieval, with references included.

Q: Why both streaming and sync APIs?
A: Streaming improves UX latency; sync provides compatibility and fallback resilience.

Q: How do you safely switch embedding models?
A: Model-specific vectorstore pathing avoids overwriting previous indexes and supports side-by-side evaluation.

## 7) 30-Second Closing

Non-technical:
Tazkiyah helps users access Quranic guidance in a natural, trustworthy, and transparent way.

Technical:
The platform already has stable contracts, deterministic orchestration, grounded retrieval, and model-switching hygiene, providing a solid base for production hardening and UX expansion.
