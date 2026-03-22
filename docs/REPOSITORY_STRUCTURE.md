# Repository Structure Reference

This document is a living map of the repository. It describes the current file structure and the intent of each top-level folder and important file.

Scope note:
- This focuses on project-owned files and folders.
- Generated caches, local vector stores, and environment folders are called out separately when they matter.
- `venv/` and `.git/` are intentionally not expanded here.

## Current Layout

```text
Tazkiyah/
- .env
- .env.example
- .gitignore
- README.md
- SETUP.md
- requirements.txt
- config.example.json
- backend/
- frontend/
- infra/
- scripts/
- docs/
- data/
- tools/
- Quran API KnowledgeBase/
```

## Root Files

- `.env`
  - Local runtime configuration for the current machine.
  - Used by the Python tooling, especially the RAG v2 pipeline.
  - Not meant to be committed.

- `.env.example`
  - Template for required environment variables.
  - Used as the starting point for a local `.env` file.

- `.gitignore`
  - Repository ignore rules.
  - Keeps generated vector stores, caches, and local-only files out of git status and commits.

- `README.md`
  - Main project entry point.
  - Explains the repo at a high level and points to the current tool layout.

- `SETUP.md`
  - Setup and verification guide.
  - Describes how to use the current Python environment and the migrated command paths.

- `requirements.txt`
  - Single Python dependency source for the whole repo.
  - Used by the collection tooling and both RAG pipelines.

- `config.example.json`
  - Example configuration for the Quran collection workflow.
  - Kept as a template for future collection runs and pipeline tuning.

## Top-Level Directories

- `backend/`
  - Reserved for future backend services.
  - No framework scaffold is created yet.
  - The goal is to keep backend concerns separate from the Python tooling.

- `frontend/`
  - Reserved for the future UI application.
  - Contains `FUTURE_WORK.md` as a placeholder reference.
  - Intended for app shell, routing, UI screens, and API client code later.

- `infra/`
  - Reserved for deployment and infrastructure assets.
  - Currently empty.

- `scripts/`
  - Reserved for helper scripts and developer shortcuts.
  - Contains `dev/` for future command wrappers.

- `docs/`
  - Repository documentation and architecture notes.
  - Stores migration notes, separation rules, and this structure reference.

- `data/`
  - Repository data area.
  - Holds raw input, processed output, samples, and vector store artifacts.

- `tools/`
  - Canonical Python tooling namespace.
  - Contains the migrated Quran collection and RAG pipelines.

- `Quran API KnowledgeBase/`
  - Curated API documentation and reference material for the Quran Foundation API.
  - Used as the source of truth for API behavior and endpoints.

## Docs Folder

- `docs/MIGRATION_PLAN.md`
  - Captures the migration strategy and transition steps.
  - Useful as historical context for the monorepo restructuring.

- `docs/SEPARATION_OF_CONCERNS.md`
  - Describes the intended boundaries between frontend, backend, tooling, and data.
  - This is the main architecture rulebook for the monorepo shape.

- `docs/REPOSITORY_STRUCTURE.md`
  - This file.
  - Explains the current layout and the purpose of each folder and important file.

## Frontend Folder

- `frontend/FUTURE_WORK.md`
  - Placeholder note for future frontend implementation.
  - Explains that no framework scaffold has been created yet.
  - Defines the intended frontend boundary.

## Scripts Folder

- `scripts/dev/README.md`
  - Placeholder note for future developer commands and wrappers.
  - Used as a landing point for local task helpers when they are added.

## Tools Folder

### `tools/python/`

- `tools/python/__init__.py`
  - Marks the Python tooling namespace.

#### `tools/python/collection/`

This folder contains the Quran collection pipeline and data preparation utilities.

- `__init__.py`
  - Marks the collection package.

- `collect_quran.py`
  - CLI entry point for collecting Quran data from the Quran Foundation API.

- `collector.py`
  - Orchestrates chapter and verse collection, footnote fetching, tafsir fetching, batching, and resume support.

- `quran_api.py`
  - Thread-safe HTTP client for the Quran Foundation API.
  - Handles retries, rate limiting, and circuit breaker behavior.

- `tafsir_fetcher.py`
  - Parallel tafsir fetcher used by the collector.
  - Adds concurrency while respecting the API client's circuit breaker state.

- `chunk_processor.py`
  - Converts raw Quran verse data into RAG-ready chunks.
  - Cleans HTML, formats footnotes, and prepares chunk text for embeddings.

- `prepare_chunks.py`
  - CLI wrapper for chunk generation.
  - Used to create chunk files from collected verse data.

- `convert_to_json.py`
  - Converts JSONL verse data into JSON array format.

- `validate_data.py`
  - Validates collected Quran data for completeness and structure.

#### `tools/python/rag_v1/`

This folder contains the legacy chunk-based RAG pipeline that is still preserved for reference and compatibility.

- `__init__.py`
  - Exposes the core RAG v1 helpers.

- `config.py`
  - Configuration for the legacy chunk-based RAG pipeline.

- `rag_pipeline.py`
  - Main RAG v1 implementation using ChromaDB and LangChain.

- `index_chunks.py`
  - CLI for indexing chunk JSONL files into the vector store.

- `query_rag.py`
  - CLI for querying the legacy RAG pipeline.

- `chat.py`
  - Terminal chat interface for RAG v1.

- `chat_ui.py`
  - Gradio-based web chat interface for RAG v1.

- `README.md`
  - Usage guide and technical notes for the legacy pipeline.

#### `tools/python/rag_v2/`

This folder contains the active RAG pipeline currently used by the project.

- `__init__.py`
  - Marks the RAG v2 package.

- `config.py`
  - Loads runtime settings from the root `.env` file.
  - Defines model, retrieval, prompt, and vector store configuration.

- `data_loader.py`
  - Loads `data/processed/rag/quran_full_rag_v2.json` and turns verses into LangChain documents.

- `rag_pipeline.py`
  - Main RAG v2 pipeline.
  - Uses the cleaned translation and commentary fields directly.

- `index_data.py`
  - CLI for indexing the processed Quran JSON into ChromaDB.

- `query_rag.py`
  - CLI for single-question retrieval against the v2 pipeline.

- `chat.py`
  - Terminal chat interface for RAG v2.

- `chat_ui.py`
  - Gradio web chat interface for RAG v2.

- `README.md`
  - Usage guide and architecture notes for the active pipeline.

- `.env.example`
  - Example environment file for RAG v2-specific settings.

## Data Folder

### `data/raw/`

- `data/raw/quran/`
  - Raw input data location.
  - Currently empty, reserved for unprocessed source material.

### `data/processed/`

- `data/processed/rag/quran_full_rag_v2.json`
  - Primary processed data file used by the active RAG v2 pipeline.
  - This is the searchable Quran dataset that the v2 indexer loads directly.

### `data/samples/`

Sample files used for testing, experimentation, and quick verification.

- `fatiha.json`
- `fatiha.jsonl`
- `fatiha.chunks.json`
- `fatiha.chunks.jsonl`

### `data/vectorstores/`

Generated vector store data for local RAG usage.

- `data/vectorstores/rag_v1/`
  - Persisted ChromaDB data for the legacy RAG v1 pipeline.
  - Contains a `chroma_db/` directory.
  - Kept locally but ignored by git.

- `data/vectorstores/rag_v2/`
  - Persisted ChromaDB data for the active RAG v2 pipeline.
  - Contains a `chroma_db_v2/` directory.
  - Kept locally but ignored by git.

## Quran API KnowledgeBase

This directory contains the project's API reference material for the Quran Foundation API.

- `quran-foundation-api-docs-structure.md`
  - High-level map of the API documentation set.

- `quran-api-docs/`
  - Folder containing endpoint-level documentation.

### `Quran API KnowledgeBase/quran-api-docs/content-apis/`

Core content endpoints and related reference pages.

- `README.md`
- `audio.md`
- `chapters.md`
- `hizb.md`
- `juz.md`
- `manzil.md`
- `quran.md`
- `resources.md`
- `rub-el-hizb.md`
- `ruku.md`
- `tafsirs.md`
- `translations.md`
- `verses.md`

### `Quran API KnowledgeBase/quran-api-docs/oauth2-apis/`

Authentication and OAuth2 endpoints.

- `README.md`
- `authorize.md`
- `introspect.md`
- `token.md`
- `userinfo.md`

### `Quran API KnowledgeBase/quran-api-docs/search-apis/`

Search-related API documentation.

- `README.md`

### `Quran API KnowledgeBase/quran-api-docs/user-apis/`

User-facing API endpoints and account features.

- `README.md`
- `activity-days.md`
- `bookmarks.md`
- `collections.md`
- `comments.md`
- `goals.md`
- `notes.md`
- `posts.md`
- `preferences.md`
- `reading-sessions.md`
- `rooms.md`
- `streaks.md`
- `tags.md`
- `users.md`

## Generated or Local-Only Items

These items are part of the working environment but are not intended as source artifacts.

- `__pycache__/`
  - Python bytecode cache directories.

- `data/vectorstores/*/chroma_db*/`
  - Generated ChromaDB persistence directories.
  - Local-only and ignored by git.

- `venv/`
  - Local Python virtual environment.
  - Used for running all Python tooling in this repo.

## Intended Organization Summary

- `frontend/` is reserved for the future UI.
- `backend/` is reserved for future API/service code.
- `tools/python/` contains the actual working Quran collection and RAG code.
- `data/` stores input, processed data, samples, and local vector stores.
- `docs/` records architecture, migration, and layout decisions.
- `Quran API KnowledgeBase/` stores API reference material needed to maintain the collection tooling.

This layout keeps concerns separated while allowing the current Python tooling to keep working from the repo root.
