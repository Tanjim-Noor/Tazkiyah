# Embedding Model Switching Workflow

This project keeps one vectorstore per embedding provider, embedding model, and collection.
That makes it safe to try different embeddings without rebuilding older stores.

## Commands

List existing stores:

```powershell
python -m tools.python.rag_v2.list_vectorstores
```

Build the current model store:

```powershell
python -m tools.python.rag_v2.build_vectorstore
```

Build a different embedding model:

```powershell
python -m tools.python.rag_v2.build_vectorstore --embedding-model "qwen3-embedding:8b"
```

`qwen3-embedding:8b` is the current default in this workspace, so it should be the first store you expect to see after a fresh build.

Verify the active path from the backend:

```powershell
curl http://127.0.0.1:8000/api/v1/config
```

## Recommended Switch Process

1. Run the list command and confirm whether the target store already exists.
2. Set `EMBEDDING_MODEL` to the model you want to evaluate. The current default is `qwen3-embedding:8b`.
3. Leave `CHROMA_PERSIST_DIR` unset unless you need a manual override.
4. Run the builder once for the target model if the store is missing.
5. Restart the backend or Gradio UI and confirm `chroma_persist_dir` in `/api/v1/config`.
6. Compare retrieval quality before deleting any older store.

## When A Model Needs Special Handling

Some embedding models need different query/document prefixes, chunk sizes, or normalization rules.
When that happens:

- Keep the storage path separate, which is already automatic here.
- Add the model-specific behavior in the RAG pipeline or a dedicated helper module.
- Record the decision in this document so the next model switch stays repeatable.
- Prefer one reusable profile per model instead of scattering special cases across scripts.
