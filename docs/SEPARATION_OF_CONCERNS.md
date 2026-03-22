# Separation of Concerns

The repository is organized as a monorepo with explicit top-level domains:
- frontend: future React + Vite + TypeScript application space
- backend: future FastAPI application space
- tools/python: preserved Quran collection and RAG tooling
- data: raw, processed, sample, and vectorstore artifacts
- docs: architecture and migration notes

Rules:
- Frontend code must not depend on Python tooling internals.
- Backend code should consume tooling through explicit service boundaries.
- Python tooling must remain runnable from the repository root during transition.
- The root requirements.txt and root venv remain the single Python package/runtime source for the repo.