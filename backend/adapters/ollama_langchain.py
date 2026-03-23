from __future__ import annotations

from typing import AsyncIterator

from langchain_ollama import ChatOllama, OllamaEmbeddings

from backend.adapters.interfaces import EmbeddingAdapter, LLMAdapter
from backend.config import Settings


class OllamaEmbeddingAdapter(EmbeddingAdapter):
    def __init__(self, settings: Settings):
        self._embeddings = OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
        )

    def embed_query(self, query: str) -> list[float]:
        return self._embeddings.embed_query(query)


class OllamaChatAdapter(LLMAdapter):
    def __init__(self, settings: Settings):
        self._settings = settings
        self._chat = ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            reasoning=False,
            temperature=settings.llm_temperature,
            num_predict=settings.llm_max_tokens,
            top_p=settings.llm_top_p,
            repeat_penalty=settings.llm_repeat_penalty,
        )

    def _build_chat(self, temperature: float | None = None) -> ChatOllama:
        if temperature is None:
            return self._chat
        # Avoid passing `temperature` through kwargs into Client.chat.
        # We instantiate a new ChatOllama object so _chat_params in langchain_ollama
        # uses the `temperature` in options instead of leaking it as an unsupported
        # top-level arg to ollama.Client.chat.
        return ChatOllama(
            model=self._settings.llm_model,
            base_url=self._settings.ollama_base_url,
            reasoning=False,
            temperature=temperature,
            num_predict=self._settings.llm_max_tokens,
            top_p=self._settings.llm_top_p,
            repeat_penalty=self._settings.llm_repeat_penalty,
        )

    def invoke(self, prompt: str, *, temperature: float | None = None) -> str:
        chat = self._build_chat(temperature)
        return str(chat.invoke(prompt).content)

    async def stream(self, prompt: str, *, temperature: float | None = None) -> AsyncIterator[str]:
        chat = self._build_chat(temperature)
        async for chunk in chat.astream(prompt):
            text = getattr(chunk, "content", "")
            if text:
                yield str(text)
