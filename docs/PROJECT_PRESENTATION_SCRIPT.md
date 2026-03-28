# Tazkiyah Project Presentation Script

Audience: mixed (technical + non-technical)
Length: 20-30 minutes
Format: talk + live demo + code walkthrough

## 1) Opening (1-2 min)

Speaker script:

Assalamu alaikum everyone. This is Tazkiyah, an AI-powered Quranic guidance platform. The core idea is simple: people describe real-life struggles in natural language, and the system responds with Quranically grounded guidance that is clear, compassionate, and source-transparent.

In this phase, we focused on building the chatbot foundation end-to-end. That means we can already receive a user question, retrieve relevant Quran context, generate a structured response, and return it through both streaming and non-streaming APIs.

## 2) Non-Technical Problem and Value (2-3 min)

Speaker script:

Many people know they should turn to the Quran for guidance, but in the moment of stress, confusion, or emotional overwhelm, they often do not know where to start. Traditional search can be hard if you do not know exact verses or Arabic terms.

Tazkiyah solves this by acting as an intelligent bridge. A user can ask in their own words, and the system maps that intent to relevant verses and returns guidance with context and references.

Non-technical value:
- Accessibility: users ask naturally, no specialized query language needed.
- Trust: responses include verse references and source metadata.
- Compassion: tone and category handling adapt to user intent.
- Reliability: when streaming is unavailable, sync fallback still works.

## 3) Technical Scope Implemented So Far (2-3 min)

Speaker script:

What is implemented right now:
- Backend API with FastAPI and LangGraph orchestration.
- Retrieval pipeline connected to Chroma vector store.
- LLM integration via Ollama adapters.
- Two chat modes:
  - Streaming SSE endpoint for real-time UX.
  - Sync JSON endpoint for broad client compatibility.
- Runtime diagnostics endpoints for health and configuration.
- Model-specific vectorstore pathing for safe embedding-model switching.

Current endpoints:
- GET /health
- GET /api/v1/config
- POST /api/v1/chat (SSE)
- POST /api/v1/chat/sync (JSON)

## 4) Architecture Story (Technical + Plain English) (4-5 min)

Speaker script:

Plain-English flow:
1. User asks a question.
2. System classifies intent (factual, emotional, or creative).
3. It retrieves the most relevant Quran context from vector search.
4. It builds a final prompt that combines user query, category instruction, and retrieved context.
5. It generates a response and streams tokens to the frontend.
6. It attaches source references so the answer remains transparent.

Technical flow:
- App startup creates services in FastAPI lifespan:
  - QuranLocalLookupService
  - RAGService
  - QuranAPITestingService
- RAGService wires:
  - OllamaEmbeddingAdapter
  - OllamaChatAdapter
  - ChromaVectorStoreAdapter
  - LangGraph orchestration graph
- Graph nodes:
  - classify
  - prompt engineering branch by category
  - retrieve context
  - finalize prompt
- Stream endpoint emits SSE events:
  - meta
  - sources
  - token (many)
  - done
  - error (if needed)

Important reliability detail:
- We added early meta event emission so frontend can confirm stream liveness quickly.
- We fixed SSE formatting to use real newline delimiters for proper client parsing.
- We sanitize model outputs to remove meta-thought leakage before showing user text.

## 5) Live Demo Plan (7-10 min)

Goal:
Show product behavior and trustworthiness, then prove backend health/config correctness.

### Demo Setup

Terminal 1: start backend

PowerShell:

& "d:/Work/Quran Project/Tazkiyah/venv/Scripts/python.exe" -m uvicorn backend.main:app --reload

### Demo Step A: Health and Runtime Config

PowerShell:

curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/config

Narration:
- Health confirms vectorstore and LLM readiness.
- Config shows active embedding model, persist directory, and vector count.
- Mention that vector_count > 0 is a key sanity signal.

### Demo Step B: Non-Streaming Chat (Safe baseline)

PowerShell:

curl -X POST "http://127.0.0.1:8000/api/v1/chat/sync" ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"I feel anxious and need guidance\",\"top_k\":5,\"temperature\":0.3,\"return_sources\":true}"

Narration:
- Show answer, category classification, and source references.
- Explain this is the compatibility fallback path.

### Demo Step C: Streaming Chat (Primary UX)

PowerShell:

curl -N -X POST "http://127.0.0.1:8000/api/v1/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"What does Surah Al-Fatihah teach about daily life?\",\"return_sources\":true}"

Narration:
- Point out event order: meta -> sources -> token stream -> done.
- Explain why streaming improves perceived responsiveness.

### Demo Step D: Embedding Model Switching (Engineering maturity)

PowerShell:

python -m tools.python.rag_v2.list_vectorstores
python -m tools.python.rag_v2.build_vectorstore --embedding-model "qwen3-embedding:8b"
curl http://127.0.0.1:8000/api/v1/config

Narration:
- We isolate stores by provider/model/collection.
- This avoids destructive overwrites and enables side-by-side retrieval evaluation.

## 6) Code Walkthrough Script (8-10 min)

Use this order while screen-sharing code.

1. Entry point and app wiring
- backend/main.py
- Explain lifespan service initialization and router registration.

2. API contracts
- backend/API_DOCUMENTATION.md
- Show endpoint responsibilities and payload shapes.

3. Chat routes
- backend/api/routes/chat.py
- Explain stream endpoint vs sync endpoint and fallback behavior.

4. Orchestration graph
- backend/graph/workflow.py
- Walk through classification -> routing -> retrieval -> final prompt assembly.

5. Core service implementation
- backend/services/rag_service.py
- Show adapters, health/runtime config, source building, streaming event emission, output sanitization.

6. Model switching reference
- docs/embedding-model-switching.md
- Explain repeatable process and operational safety.

## 7) Suggested Slide Deck Structure (10-12 slides)

1. Project title and one-line mission
2. Problem and why now
3. User journey (before vs after)
4. What we built in this phase
5. System architecture overview
6. API contract and integration modes
7. Live demo (health/config/chat stream)
8. Reliability and observability improvements
9. Embedding-model switching workflow
10. Current limitations and risks
11. Next roadmap steps
12. Closing and Q&A

## 8) Non-Technical Closing (1 min)

Speaker script:

Tazkiyah is not just a chatbot. It is a trust-first guidance experience. In this phase, we proved the foundation: stable APIs, transparent sourcing, and resilient response modes. Next, we turn this strong backend core into a polished product experience with reflection workflows and personalized growth features.

## 9) Technical Closing (1 min)

Speaker script:

From an engineering standpoint, we now have:
- Clear service boundaries and adapters.
- Deterministic orchestration flow in LangGraph.
- Streaming plus sync fallback with hardened SSE behavior.
- Model-specific vectorstore lifecycle for safe experimentation.

This gives us a stable platform to scale both product features and model experimentation without architectural rewrites.

## 10) Q&A Cheat Sheet

Q: How do you prevent hallucinations?
A: We ground responses in retrieved Quran context, return explicit source references, and keep retrieval diagnostics visible through config and vector counts.

Q: What if streaming fails?
A: Sync endpoint remains available, and backend emits structured errors for graceful fallback handling.

Q: How do you compare embedding quality?
A: Each model has its own vectorstore path; we switch model config, build once, and validate retrieval outcomes without deleting prior stores.

Q: What is production readiness status?
A: Core chatbot pipeline is working; next steps are UX hardening, contract freeze, and expanded test coverage under load.
