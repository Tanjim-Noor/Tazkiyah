# Progress Report - Chatbot Initial Phase

Date: 2026-03-24
Project: Tazkiyah (Quranic Guidance Platform)
Audience: LLM-assisted design brainstorming (pre-Stitch design handoff)

## 1) Ultimate Goal (from README)
Build an AI-powered Quranic guidance experience where users can describe real-life struggles in natural language and receive Quranically grounded guidance with context, compassion, and clarity.

For the current initial phase, the practical goal is:
- Deliver a reliable chatbot core that can receive user questions, retrieve relevant Quran context, generate answers, and stream responses to the frontend.

## 2) Scope of This Report
This report covers only the chatbot initial phase (backend + frontend integration readiness), not the full product roadmap (journaling, community features, dashboards, etc.).

## 3) What Is Already Done

### 3.1 Non-Technical Summary
- A working chatbot foundation exists end-to-end.
- The system can answer Quran-guidance questions through both streaming and non-streaming modes.
- The frontend has enough architecture and diagnostics to support design work next, instead of redoing API integration later.
- Major streaming reliability issue has been investigated and fixed at the backend formatter level.

### 3.2 Technical Summary
- Backend API foundation is implemented with FastAPI + LangGraph:
  - GET /health
  - GET /api/v1/config
  - POST /api/v1/chat (SSE streaming)
  - POST /api/v1/chat/sync (JSON fallback)
- Retrieval + generation pipeline is connected:
  - Chroma vector store adapter
  - Ollama chat and embedding adapters
  - Category-aware orchestration graph
- Frontend integration scaffold is implemented:
  - React + Vite + TypeScript
  - TanStack Query for bootstrap state (health/config)
  - Chat flow with SSE primary and sync fallback
- Observability/tracing is in place:
  - Client-side request-scoped logs
  - Lifecycle diagnostics and flow trace UI panel
  - Backend route-level error logging for chat endpoints
- Backend resilience improvements completed:
  - Structured 503 sync error responses when backend dependencies are unavailable
  - Early meta event emission in stream path
- Streaming root-cause fix completed:
  - SSE formatting corrected to use real newline delimiters (not escaped literals), enabling proper incremental client parsing.

## 4) Current State Assessment

### 4.1 What Works Reliably
- Backend responds and can generate answers.
- Sync fallback path is functional and debuggable.
- SSE stream frames are now formatted correctly for frontend parsing.
- Build/lint/typecheck baseline has been stabilized during implementation.

### 4.2 Remaining Gaps in Initial Phase
- Need repeated real-user verification that streaming UX is consistently smooth (not only technically valid).
- Need clear user-facing loading/error states finalized for production UX.
- Need final API contract freeze for fields/events before visual design iteration accelerates.

## 5) Next Steps (Initial Chatbot Phase Only)

### 5.1 Non-Technical Next Steps
- Confirm the chatbot experience is trustworthy from a user perspective:
  - Fast perceived response start
  - Clear progress indicators
  - Clear fallback behavior when streaming is slow
- Lock the chatbot interaction model before visual polishing:
  - Message states
  - Source display style
  - Error and retry UX
- Prepare a design-ready brief so Stitch design sessions can focus on UX and visual quality rather than backend uncertainty.

### 5.2 Technical Next Steps
- Streaming hardening and verification:
  - Run repeated end-to-end SSE tests under normal and stressed conditions.
  - Track time-to-first-event and timeout/fallback rate.
  - Add/confirm keepalive strategy if long model latency appears in production-like tests.
- Frontend UX contract stabilization:
  - Finalize event/state mapping for: connecting, streaming, done, error, fallback.
  - Standardize source attribution rendering and empty/error edge cases.
- Backend readiness checks:
  - Ensure dependency readiness (LLM/vectorstore) is surfaced clearly and used consistently by frontend gating logic.
  - Add lightweight smoke tests for chat stream + sync endpoints.
- Pre-design technical freeze for chatbot phase:
  - Freeze request/response schema and SSE event contract.
  - Freeze minimum diagnostics needed in dev builds.

## 6) Suggested Inputs for LLM Brainstorming (Before Stitch)
Use this context when brainstorming design direction:
- Product promise: compassionate Quranic guidance for real-life struggles.
- Current constraints: chatbot-first, API contracts mostly in place, stream + fallback model.
- Design objective: emotionally calm, trustworthy, readable, and source-transparent conversation UI.
- Must include:
  - First-message empty state
  - Streaming message behavior
  - Source/verse cards
  - Error and retry patterns
  - Fallback communication (without technical jargon)

## 7) Definition of Done for Initial Chatbot Phase
- User can ask a question and reliably receive a useful answer.
- Streaming works for normal cases; fallback handles degraded cases gracefully.
- Quran source references are visible and understandable.
- Core interaction states are stable and documented for design implementation.
- Team is ready to move into Stitch-led UI design and implementation confidently.
