# Chat Feature Module

## Purpose

Implements runtime chat integration with backend SSE and sync fallback.

## Public API

- `useChat()` from `hooks/useChat.ts`
- `Chat` container from `components/Chat.tsx`

## Internal Boundaries

- `services/chatAPI.ts` performs transport and request normalization.
- `components/*` are presentation and container logic for chat only.
- `types/*` are feature-local UI state contracts.

## Stitch Handoff Notes

- Keep hook signatures stable.
- Keep component props explicit and typed.
- Avoid embedding design-system assumptions in component logic.
