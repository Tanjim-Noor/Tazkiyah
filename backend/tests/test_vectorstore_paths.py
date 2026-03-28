from __future__ import annotations

from pathlib import Path

from tools.python.rag_v2.vectorstore_paths import get_vectorstore_persist_directory


def test_vectorstore_directory_changes_with_embedding_model() -> None:
    root_dir = Path("d:/tmp/vectorstores")

    first_path = get_vectorstore_persist_directory(
        embedding_provider="ollama",
        embedding_model="qwen3-embedding:8b",
        collection_name="quran_tazkiyah_v2",
        root_dir=root_dir,
    )
    second_path = get_vectorstore_persist_directory(
        embedding_provider="ollama",
        embedding_model="jina/jina-embeddings-v2-base-en",
        collection_name="quran_tazkiyah_v2",
        root_dir=root_dir,
    )

    assert first_path != second_path
    assert "qwen3-embedding-8b" in str(first_path)
    assert "jina-embeddings-v2-base-en" in str(second_path)


def test_vectorstore_directory_uses_explicit_override() -> None:
    explicit_dir = Path("d:/tmp/custom/vectorstore")

    resolved = get_vectorstore_persist_directory(
        embedding_provider="ollama",
        embedding_model="nomic-embed-text-v2-moe",
        collection_name="quran_tazkiyah_v2",
        explicit_persist_dir=explicit_dir,
    )

    assert resolved == explicit_dir.resolve()
