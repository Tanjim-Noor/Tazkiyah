from __future__ import annotations

import json
import re
from collections.abc import AsyncIterator

from backend.adapters.chroma_langchain import ChromaVectorStoreAdapter
from backend.adapters.ollama_langchain import OllamaChatAdapter, OllamaEmbeddingAdapter
from backend.config import Settings
from backend.graph.workflow import build_orchestration_graph, configure_langsmith_environment
from backend.services.quran_local_lookup_service import QuranLocalLookupService


class LLMOutputSanitizer:
    """Remove model meta-thought leakage from user-facing responses."""

    _meta_patterns = (
        r"\bwait\s*,?\s*i\s+must\b",
        r"\blet\s+me\s+check\b",
        r"\blet\s+me\s+re-?read\b",
        r"\bupon\s+reviewing\b",
        r"\bi\s+must\s+check\s+the\s+provided\s+context\b",
        r"\bprovided\s+context\b",
        r"\bcontext\s+provided\s+in\s+the\s+prompt\b",
        r"\bin\s+the\s+prompt\b",
        r"\bcitation\s+contract\b",
        r"\bresponse\s+shape\b",
        r"\bsystem\s+instruction\b",
        r"\bfinal\s+check\s+before\s+responding\b",
        r"\bto\s+strictly\s+adhere\s+to\s+the\s+rule\b",
        r"\bi\s+will\s+only\s+cite\s+verses\s+explicitly\b",
    )
    _meta_prefixes = (
        "wait",
        "let me",
        "upon reviewing",
        "i must",
        "provided context",
        "context provided",
        "in the prompt",
        "citation contract",
        "response shape",
        "system instruction",
        "final check",
        "to strictly adhere",
        "i will only cite",
    )

    def __init__(self) -> None:
        self._line_buffer = ""
        self._in_think_block = False
        self._meta_regex = re.compile("|".join(self._meta_patterns), flags=re.IGNORECASE)

    def process_chunk(self, chunk: str) -> str:
        if not chunk:
            return ""
        without_think = self._strip_think_blocks(chunk)
        return self._filter_lines(without_think, final=False)

    def finalize(self) -> str:
        return self._filter_lines("", final=True)

    def sanitize_text(self, text: str) -> str:
        if not text:
            return ""
        self._line_buffer = ""
        self._in_think_block = False
        cleaned = self.process_chunk(text)
        tail = self.finalize()
        return (cleaned + tail).strip()

    def _strip_think_blocks(self, text: str) -> str:
        if not text:
            return ""

        result: list[str] = []
        i = 0
        lower_text = text.lower()

        while i < len(text):
            if self._in_think_block:
                end = lower_text.find("</think>", i)
                if end == -1:
                    return "".join(result)
                i = end + len("</think>")
                self._in_think_block = False
                continue

            start = lower_text.find("<think>", i)
            if start == -1:
                result.append(text[i:])
                break

            result.append(text[i:start])
            i = start + len("<think>")
            self._in_think_block = True

        return "".join(result)

    def _filter_lines(self, text: str, *, final: bool) -> str:
        combined = f"{self._line_buffer}{text}"
        lines = combined.splitlines(keepends=True)

        if not final and lines and not lines[-1].endswith(("\n", "\r")):
            tail = lines.pop()
            if self._should_buffer_incomplete_line(tail):
                self._line_buffer = tail
            else:
                self._line_buffer = ""
                lines.append(tail)
        else:
            self._line_buffer = ""

        output: list[str] = []
        for line in lines:
            if self._is_meta_line(line):
                continue
            output.append(line)

        return "".join(output)

    def _is_meta_line(self, line: str) -> bool:
        normalized = " ".join(line.strip().lower().split())
        if not normalized:
            return False
        return bool(self._meta_regex.search(normalized))

    def _should_buffer_incomplete_line(self, line: str) -> bool:
        normalized = " ".join(line.strip().lower().split())
        if not normalized:
            return False
        return normalized.startswith(self._meta_prefixes)


class RAGService:
    def __init__(
        self,
        settings: Settings,
        *,
        quran_lookup_service: QuranLocalLookupService | None = None,
    ):
        self.settings = settings
        self.quran_lookup_service = quran_lookup_service

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
            "chroma_persist_dir": str(self.settings.chroma_persist_dir),
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

    def _build_sources(self, state: dict, *, return_sources: bool) -> list[dict]:
        if not return_sources:
            return []

        sources: list[dict] = []
        documents = state.get("documents", [])
        scores = state.get("scores", [])

        for idx, doc in enumerate(documents):
            metadata = doc.metadata or {}
            score = scores[idx] if idx < len(scores) else None

            verse_id = metadata.get("verse_id", "")
            verse_key = metadata.get("verse_key") or verse_id
            lookup = self.quran_lookup_service.get_verse(verse_key) if self.quran_lookup_service else None

            sources.append(
                {
                    "verse_id": verse_id,
                    "verse_key": verse_key,
                    "surah_name": metadata.get("surah_name") or (lookup or {}).get("surah_name"),
                    "surah_number": metadata.get("surah_number") or (lookup or {}).get("surah_number"),
                    "verse_number": metadata.get("verse_number") or (lookup or {}).get("verse_number"),
                    "score": score,
                    "arabic_text": (lookup or {}).get("arabic_text"),
                    "translation": (lookup or {}).get("translation"),
                }
            )

        return sources

    async def stream_answer(
        self,
        *,
        query: str,
        top_k: int | None,
        temperature: float | None,
        return_sources: bool,
    ) -> AsyncIterator[dict]:
        # Emit an early metadata event so streaming clients can confirm the
        # connection is alive before graph retrieval/assembly completes.
        provisional_category = self.settings.category_factual
        yield {"event": "meta", "data": {"category": provisional_category}}

        state = self._run_graph(query, top_k_override=top_k)
        category = state.get("category", self.settings.category_factual)
        sources = self._build_sources(state, return_sources=return_sources)

        if category != provisional_category:
            yield {"event": "meta", "data": {"category": category}}

        if sources:
            # Emit sources before token streaming to support non-blocking UI placeholders.
            yield {"event": "sources", "data": {"sources": sources}}

        answer_chunks: list[str] = []
        sanitizer = LLMOutputSanitizer()
        async for chunk in self.llm_adapter.stream(
            state.get("final_prompt", ""),
            temperature=temperature,
        ):
            safe_chunk = sanitizer.process_chunk(chunk)
            if not safe_chunk:
                continue
            answer_chunks.append(safe_chunk)
            yield {"event": "token", "data": {"text": safe_chunk}}

        tail = sanitizer.finalize()
        if tail:
            answer_chunks.append(tail)
            yield {"event": "token", "data": {"text": tail}}

        answer = "".join(answer_chunks)

        yield {
            "event": "done",
            "data": {
                "answer": answer,
                "category": category,
                "sources": sources,
            },
        }
    def answer(
        self,
        *,
        query: str,
        top_k: int | None,
        temperature: float | None,
        return_sources: bool,
    ) -> dict:
        state = self._run_graph(query, top_k_override=top_k)
        category = state.get("category", self.settings.category_factual)

        answer = self.llm_adapter.invoke(
            state.get("final_prompt", ""),
            temperature=temperature,
        )
        answer = LLMOutputSanitizer().sanitize_text(answer)

        sources = self._build_sources(state, return_sources=return_sources)

        return {
            "answer": answer,
            "category": category,
            "sources": sources,
        }
    @staticmethod
    def format_sse(event: str, payload: dict) -> str:
        return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
