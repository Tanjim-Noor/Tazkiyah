---
name: switch-embedding-model
description: Switch the Tazkiyah RAG embedding model, research model-specific behavior, and update the vectorstore/config for the selected model.
---

# Switch Embedding Model

Use this prompt when I want to change the embedding model used by the Tazkiyah RAG pipeline.
The model name will be provided in the prompt arguments.

## Input

- Target embedding model: `$ARGUMENTS`

## Workflow

1. Identify the target embedding model from `$ARGUMENTS` and determine whether the provider must change too.
2. Research the model online and in the workspace for any special instructions, such as:
   - query/document prefixes
   - normalization rules
   - chunking or context-length constraints
   - provider-specific requirements
   - known retrieval use cases or limitations
3. List existing vectorstores with `python -m tools.python.rag_v2.list_vectorstores`.
4. Decide whether the target store already exists.
5. Update environment or config values only where needed:
   - `EMBEDDING_MODEL`
   - `EMBEDDING_PROVIDER`
   - `VECTORSTORE_ROOT_DIR` only if I explicitly want a different root
   - leave `CHROMA_PERSIST_DIR` unset unless a manual override is required
6. Build the target vectorstore once if it is missing:
   - `python -m tools.python.rag_v2.build_vectorstore --embedding-model "$ARGUMENTS"`
7. Verify the backend now points at the expected store:
   - `GET /api/v1/config`
8. If the model needs special handling, update the RAG pipeline or a dedicated model-profile helper instead of scattering one-off logic.
9. Update [docs/embedding-model-switching.md](../../docs/embedding-model-switching.md) if the model requires special behavior or a non-default workflow.

## Completion Criteria

- The target model is researched.
- The vectorstore exists or is built once.
- The resolved `chroma_persist_dir` matches the new model.
- Any model-specific behavior is documented.
- The workspace remains safe to switch back and forth without rebuilding unrelated stores.
