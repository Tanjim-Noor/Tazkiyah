# Frontend Next Steps (Phase 1 Scope)

This file defines a small, realistic frontend subset focused on full backend chat integration first.

Backend APIs available now:
- `GET /health`
- `GET /api/v1/config`
- `POST /api/v1/chat` (SSE streaming)
- `POST /api/v1/chat/sync` (JSON fallback only)

## Goal

Ship a fully working streaming chatbot (SSE) with strong backend integration and reliability checks.

## In Scope (Build Now: Backend Integration First)

1. Backend Connectivity Bootstrap
- On app load, call `/health` and `/api/v1/config`.
- Surface backend readiness clearly:
  - Healthy if status is ok and vector_count > 0.
  - Warning if status is degraded or vector_count == 0.
- Block chat send if backend is unavailable.

2. Streaming Chat (Primary Path)
- Use `POST /api/v1/chat` as the main chat flow.
- Implement full SSE event handling:
  - meta
  - token
  - done
  - error
- Build message state so token events append progressively to the active assistant response.
- Finalize answer and sources only on done event.

3. Request Controls + Validation
- Chat request supports:
  - query (required)
  - top_k (optional)
  - temperature (optional)
  - return_sources (optional)
- Clamp client values before submit:
  - top_k: 1..20
  - temperature: 0.0..2.0

4. Core Runtime States
- Loading state while waiting for chat response.
- Streaming state while tokens are arriving.
- Disabled send button on empty query or active request.
- Cancel-in-flight behavior (AbortController) for long streams.
- Error banner for network/API failures and SSE parse errors.

5. SSE Reliability + Fallback
- Handle incomplete/terminated streams safely.
- Guard against duplicate done events.
- Keep POST `/api/v1/chat/sync` as manual fallback for debugging only.

## Out of Scope (Later Phases)

- UI component/design system work.
- Visual polish and advanced UX styling.
- Reflection journal and mood tracking.
- Bookmark system and saved verse workflows.
- Community wisdom wall.
- Progress dashboard and streak analytics.
- Personalized verse-of-the-day.
- Authentication and user profiles.
- Full PWA/offline architecture.
- Frontend session persistence/history restoration.

## Phase 1 Delivery Checklist

- [ ] Health and config bootstrap on app start
- [ ] Chat form wired to `POST /api/v1/chat` (SSE)
- [ ] SSE event parser implemented (`meta`, `token`, `done`, `error`)
- [ ] Progressive token rendering implemented
- [ ] Final answer/category/sources commit on `done`
- [ ] Stream cancellation and retry behavior implemented
- [ ] SSE failure fallback path to `POST /api/v1/chat/sync` available

## Suggested Build Order

1. API client layer
- Create typed API functions for health/config/chat-stream (+ optional sync fallback).
- Centralize base URL in one config file.

2. App state
- Introduce minimal state model:
  - backendStatus
  - config
  - messages
  - isStreaming
  - error

3. Streaming engine
- Implement SSE reader pipeline using fetch + ReadableStream.
- Parse event chunks safely and dispatch to state reducer.
- Support cancellation and cleanup on unmount.

4. Runtime hardening
- Retry action on failure.
- Add fallback call to sync endpoint for diagnostics.
- Validate end-to-end behavior against backend docs.

## Optional Step After Phase 1

After streaming is stable, proceed to design/UI work and broader feature layers.
