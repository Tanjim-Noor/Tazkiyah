from __future__ import annotations

import json
from collections.abc import AsyncIterator

from backend.adapters.chroma_langchain import ChromaVectorStoreAdapter
from backend.adapters.ollama_langchain import OllamaChatAdapter, OllamaEmbeddingAdapter
from backend.config import Settings
from backend.graph.workflow import build_orchestration_graph, configure_langsmith_environment


class RAGService:
    def __init__(self, settings: Settings):
        self.settings = settings

        configure_langsmith_environment(settings)

        self.embedding_adapter = OllamaEmbeddingAdapter(settings)
        self.llm_adapter = OllamaChatAdapter(settings)
        self.vector_adapter = ChromaVectorStoreAdapter(
            settings,
            embedding_function=self.embedding_adapter._embeddings,
        )
        self.graph = build_orchestration_graph(
            settings,
            llm_adapter=self.llm_adapter,
            vector_adapter=self.vector_adapter,
        )

    def health(self) -> dict:
        vector_ok = False
        llm_ok = False

        try:
            _ = self.vector_adapter.count()
            vector_ok = True
        except Exception:
            vector_ok = False

        try:
            _ = self.llm_adapter.invoke("Reply with: ok", temperature=0.0)
            llm_ok = True
        except Exception:
            llm_ok = False

        return {
            "status": "ok" if vector_ok and llm_ok else "degraded",
            "service": "tazkiyah-backend",
            "vectorstore_ready": vector_ok,
            "llm_ready": llm_ok,
        }

    def runtime_config(self) -> dict:
        return {
            "app_name": self.settings.app_name,
            "environment": self.settings.app_env,
            "llm_provider": self.settings.llm_provider,
            "embedding_provider": self.settings.embedding_provider,
            "vectorstore_provider": self.settings.vectorstore_provider,
            "llm_model": self.settings.llm_model,
            "embedding_model": self.settings.embedding_model,
            "collection_name": self.settings.collection_name,
            "top_k": self.settings.top_k,
            "categories": list(self.settings.categories),
            "langsmith_tracing": self.settings.langsmith_tracing,
            "langsmith_project": self.settings.langsmith_project,
            "vector_count": self.vector_adapter.count(),
        }

    def _run_graph(self, query: str, top_k_override: int | None = None) -> dict:
        original_top_k = self.settings.top_k
        if top_k_override is not None:
            self.settings.top_k = top_k_override

        try:
            state = self.graph.invoke({"query": query})
        finally:
            self.settings.top_k = original_top_k

        return state

    async def stream_answer(
        self,
        *,
        query: str,
        top_k: int | None,
        temperature: float | None,
        return_sources: bool,
    ) -> AsyncIterator[dict]:
        state = self._run_graph(query, top_k_override=top_k)
        category = state.get("category", self.settings.category_factual)

        yield {"event": "meta", "data": {"category": category}}

        answer_chunks: list[str] = []
        async for chunk in self.llm_adapter.stream(
            state.get("final_prompt", ""),
            temperature=temperature,
        ):
            answer_chunks.append(chunk)
            yield {"event": "token", "data": {"text": chunk}}

        answer = "".join(answer_chunks)

        sources = []
        if return_sources:
            documents = state.get("documents", [])
            scores = state.get("scores", [])
            for idx, doc in enumerate(documents):
                metadata = doc.metadata or {}
                score = scores[idx] if idx < len(scores) else None
                sources.append(
                    {
                        "verse_id": metadata.get("verse_id", ""),
                        "surah_name": metadata.get("surah_name"),
                        "surah_number": metadata.get("surah_number"),
                        "verse_number": metadata.get("verse_number"),
                        "score": score,
                    }
                )

        yield {
            "event": "done",
            "data": {
                "answer": answer,
                "category": category,
                "sources": sources,
            },
        }

    @staticmethod
    def format_sse(event: str, payload: dict) -> str:
        return f"event: {event}\\ndata: {json.dumps(payload, ensure_ascii=False)}\\n\\n"
