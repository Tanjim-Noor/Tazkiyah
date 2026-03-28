from __future__ import annotations

import os
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_VECTORSTORE_ROOT = PROJECT_ROOT / "data" / "vectorstores" / "rag_v2"


def slugify_path_component(value: str) -> str:
    """Convert a model or provider name into a filesystem-safe path component."""
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    return normalized or "default"


def get_vectorstore_persist_directory(
    *,
    embedding_provider: str,
    embedding_model: str,
    collection_name: str,
    root_dir: Path | None = None,
    explicit_persist_dir: str | Path | None = None,
) -> Path:
    """Resolve the Chroma persist directory for a given embedding model.

    The resolved path changes automatically when the embedding provider or model
    changes, which keeps each embedding-backed store isolated.
    """

    if explicit_persist_dir:
        return Path(explicit_persist_dir).expanduser().resolve()

    root_path = Path(root_dir or os.getenv("VECTORSTORE_ROOT_DIR", DEFAULT_VECTORSTORE_ROOT))
    provider_slug = slugify_path_component(embedding_provider)
    model_slug = slugify_path_component(embedding_model)
    collection_slug = slugify_path_component(collection_name)
    return root_path / provider_slug / model_slug / collection_slug


def discover_vectorstore_directories(root_dir: Path | None = None) -> list[Path]:
    """Return discovered model-specific vectorstore directories under a root."""

    root_path = Path(root_dir or os.getenv("VECTORSTORE_ROOT_DIR", DEFAULT_VECTORSTORE_ROOT)).expanduser().resolve()
    if not root_path.exists():
        return []

    discovered: set[Path] = set()
    for sqlite_file in root_path.rglob("chroma.sqlite3"):
        collection_dir = sqlite_file.parent
        try:
            relative_parts = collection_dir.relative_to(root_path).parts
        except ValueError:
            continue

        if len(relative_parts) != 3:
            continue

        discovered.add(collection_dir)

    return sorted(discovered)
