# Chatbot New Feature

This feature hosts a new, isolated chatbot page at `/chatbot-new`.

## Purpose

Provide a design-first chatbot experience that can evolve independently from the current integration page (`/`).

## Boundaries

- Reuses existing API contracts and streaming behavior.
- Imports shared TanStack bootstrap hooks: `useHealthQuery` and `useConfigQuery`.
- Imports existing chat API utilities from `features/chat/services/chatAPI`.
- Keeps existing `/` page logic untouched.
- Maintains independent local UI state via `useChatbotNew` (no local state sharing with `/`).
- Allows iterative visual redesign for Stitch-driven handoff.

## Public Surface

- `components/ChatbotNewPage.tsx`
- `components/ChatbotNewChat.tsx`
- `constants/index.ts`
- `hooks/useChatbotNew.ts`
- `types/index.ts`
