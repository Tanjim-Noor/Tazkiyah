from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from backend.adapters.interfaces import VectorStoreAdapter
from backend.config import Settings


class ChromaVectorStoreAdapter(VectorStoreAdapter):
    def __init__(self, settings: Settings, embedding_function):
        self._settings = settings
        self._store = Chroma(
            collection_name=settings.collection_name,
            persist_directory=str(Path(settings.chroma_persist_dir)),
            embedding_function=embedding_function,
        )

    def similarity_search_with_score(self, query: str, k: int) -> list[tuple[Document, float]]:
        return self._store.similarity_search_with_score(query, k=k)

    def count(self) -> int:
        return self._store._collection.count()
