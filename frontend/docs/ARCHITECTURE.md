# Frontend Architecture (Phase 1)

## Layers
- Shell: `main.tsx`, `App.tsx`, `providers`
- Config: `config`
- Shared: `common`, `components`
- Domain: `features/chat`

## Import Rules
- `common` must not import from `features`.
- `features/chat` can import from `common` and `components`.
- Service modules remain framework-agnostic.

## State Split
- Server-state: React Query (`health`, `config`).
- Stream session-state: feature hook (`useChat`).

## Design Handoff Note
UI components intentionally remain minimal and typed so visual redesign can proceed without refactoring API and streaming logic.
