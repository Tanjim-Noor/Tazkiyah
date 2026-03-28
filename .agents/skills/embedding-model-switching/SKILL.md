---
name: embedding-model-switching
description: |
  Workflow for switching embedding models in the Tazkiyah RAG pipeline.
  Use when: the user wants to change EMBEDDING_MODEL, compare or list vectorstores,
  research a specific embedding model, build a model-specific Chroma store,
  or update model-specific retrieval behavior and config.
---

# Embedding Model Switching

Use this workflow when changing embedding models in the Tazkiyah RAG stack.
The goal is to evaluate a model, keep its vectorstore isolated, and update only
the config or code that actually changes for that model.

## Standard Workflow

1. Inventory the current state.
   - Run `python -m tools.python.rag_v2.list_vectorstores`.
   - Check the active runtime config with `GET /api/v1/config`.
   - Confirm whether `CHROMA_PERSIST_DIR` is intentionally overriding the derived path.
2. Research the target model before changing code.
   - Use the workspace docs first, then search vendor docs or model cards for the exact model name.
   - Look for provider compatibility, expected input normalization, query/document prefixes, context length, batching guidance, and any model-specific retrieval notes.
   - If the model requires a different provider than the current one, stop and update the adapter layer first.
3. Decide whether the model needs a profile change or just a path change.
   - If only the embedding model changes, update env/config and reuse the model-specific vectorstore layout.
   - If the model also needs different prefixes, chunking, or normalization, update the RAG pipeline or a dedicated profile helper.
4. Apply the change in the workspace.
   - Update `.env` or environment-driven defaults when needed.
   - Keep `CHROMA_PERSIST_DIR` unset unless a manual override is truly required.
   - Let the derived path resolve to `data/vectorstores/rag_v2/<provider>/<model>/<collection>`.
5. Build or reuse the vectorstore.
   - Run `python -m tools.python.rag_v2.build_vectorstore --embedding-model "MODEL_NAME"`.
   - If the store already exists, reuse it and do not rebuild unless the model or data changed.
6. Validate the switch.
   - Re-check `GET /api/v1/config`.
   - Compare retrieval quality with the previous model.
   - Run the backend tests if config, path logic, or adapter code changed.
7. Record model-specific behavior.
   - Update `docs/embedding-model-switching.md` when the model needs special handling.
   - Keep the note brief and specific so the next switch is repeatable.

## Model-Specific Rules

- Keep one Chroma directory per provider/model/collection combination.
- Do not reuse an old vectorstore path for a new embedding model unless compatibility is proven.
- Prefer one reusable profile per model rather than scattering special cases across scripts.
- If the model needs custom query or document prefixes, keep that logic in the RAG pipeline or a profile helper.
- If chunking, metadata, normalization, or provider selection changes with the model, document the reason before promoting the switch.

## Commands To Prefer

- List stores: `python -m tools.python.rag_v2.list_vectorstores`
- Build the current model store: `python -m tools.python.rag_v2.build_vectorstore`
- Build a specific model: `python -m tools.python.rag_v2.build_vectorstore --embedding-model "MODEL_NAME"`
- Check runtime config: `GET /api/v1/config`

## Suggested Prompt For Future Work

Use this when asking an agent to switch models safely:

> List the existing vectorstores, research the target embedding model and provider docs, determine whether it needs special prefixes or normalization, update the runtime config only as needed, build or reuse the matching model-specific store, and document any model-specific retrieval behavior such as prefixes, chunking, or normalization.
