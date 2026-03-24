## Plan: Frontend API Integration and Design-Ready Scaffold

Deliver a lean frontend integration layer that is fully wired to backend APIs, follows selective layered architecture patterns, supports SSE-first chat with sync fallback, and keeps UI minimal for Stitch handoff.

## Current Decisions

- SSE as primary transport with automatic sync fallback.
- TanStack Query for bootstrap/server state.
- No Redux/routing/i18n in this phase.
- Keep styling minimal and postpone design-system work.

## Layered Structure

- Layer 0 (shell): `main.tsx`, `App.tsx`, `providers`, `styles`
- Layer 1 (config): `config` for env binding, API setup, error boundary
- Layer 2 (shared): `common`, `components`
- Layer 3 (domain): `features/chat`

## Phases

1. Foundation: structure, providers, env/config setup.
2. Contracts: shared types and constants.
3. Services: framework-agnostic HTTP + SSE parsing + normalization.
4. State: React Query hooks and chat streaming orchestration hook.
5. UI: minimal runtime bootstrap + chat integration test surface.
6. Hardening: architecture docs and feature boundary docs.
7. Verification: lint/typecheck/build + manual integration scenarios.

## Implementation Tracking Markdown Files

When implementation starts, progress is tracked in this folder:

- `frontend/plan/IMPLEMENTATION_LOG.md`
- `frontend/plan/PHASE_1_STRUCTURE.md`
- `frontend/plan/PHASE_2_CONTRACTS.md`
- `frontend/plan/PHASE_3_SERVICES.md`
- `frontend/plan/PHASE_4_STATE.md`
- `frontend/plan/PHASE_5_UI.md`
- `frontend/plan/PHASE_6_HARDENING.md`
- `frontend/plan/PHASE_7_VERIFICATION.md`

## Verification Targets

- Bootstrap `/health` and `/api/v1/config` successfully.
- Stream tokens from `/api/v1/chat` and finalize on `done`.
- Fall back to `/api/v1/chat/sync` on stream failure.
- Support cancellation without stale UI state.
- Clamp `top_k` and `temperature` to backend constraints.
- Preserve architectural boundaries and separation of concerns.