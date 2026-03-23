from __future__ import annotations

from abc import ABC, abstractmethod

from langchain_core.documents import Document


class EmbeddingAdapter(ABC):
    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        raise NotImplementedError


class LLMAdapter(ABC):
    @abstractmethod
    def invoke(self, prompt: str, *, temperature: float | None = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream(self, prompt: str, *, temperature: float | None = None):
        raise NotImplementedError


class VectorStoreAdapter(ABC):
    @abstractmethod
    def similarity_search_with_score(self, query: str, k: int) -> list[tuple[Document, float]]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError
