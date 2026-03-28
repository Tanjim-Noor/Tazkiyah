from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from tools.python.rag_v2.vectorstore_paths import (
    DEFAULT_VECTORSTORE_ROOT,
    get_vectorstore_persist_directory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Runtime settings for the FastAPI + LangGraph backend."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Tazkiyah Backend"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    log_level: str = "INFO"

    llm_provider: str = "ollama"
    embedding_provider: str = "ollama"
    vectorstore_provider: str = "chroma"

    llm_model: str = Field(default="gemma3:4b", alias="LLM_MODEL")
    embedding_model: str = Field(default="qwen3-embedding:8b", alias="EMBEDDING_MODEL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")

    collection_name: str = Field(default="quran_tazkiyah_v2", alias="COLLECTION_NAME")
    vectorstore_root_dir: Path = Field(
        default=DEFAULT_VECTORSTORE_ROOT,
        alias="VECTORSTORE_ROOT_DIR",
    )
    chroma_persist_dir: Path | None = Field(default=None, alias="CHROMA_PERSIST_DIR")
    rag_data_file: Path = Field(
        default=PROJECT_ROOT / "data" / "processed" / "rag" / "quran_full_rag_v2.json",
        alias="RAG_DATA_FILE",
    )
    quran_raw_data_dir: Path = Field(
        default=PROJECT_ROOT / "data" / "raw" / "quran" / "source",
        alias="QURAN_RAW_DATA_DIR",
    )
    quran_default_translation_language: str = Field(
        default="en",
        alias="QURAN_DEFAULT_TRANSLATION_LANGUAGE",
    )

    top_k: int = Field(default=3, alias="TOP_K")
    min_relevance_score: float = Field(default=0.0, alias="MIN_RELEVANCE_SCORE")

    llm_temperature: float = Field(default=0.3, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=1024, alias="LLM_MAX_TOKENS")
    llm_top_p: float = Field(default=0.9, alias="LLM_TOP_P")
    llm_repeat_penalty: float = Field(default=1.1, alias="LLM_REPEAT_PENALTY")

    langsmith_tracing: bool = Field(default=True, alias="LANGSMITH_TRACING")
    langsmith_api_key: str = Field(default="", alias="LANGSMITH_API_KEY")
    langsmith_project: str = Field(default="tazkiyah-backend", alias="LANGSMITH_PROJECT")
    langsmith_endpoint: str = Field(
        default="https://api.smith.langchain.com",
        alias="LANGSMITH_ENDPOINT",
    )

    cors_allowed_origins: list[str] = ["*"]

    category_factual: str = "Factual & Informational"
    category_emotional: str = "Emotional & Empathetic"
    category_creative: str = "Creative"

    base_system_prompt: str = (
        "You are Tazkiyah, an Islamic assistant grounded in Quranic content. "
        "Answer using the provided retrieval context and cite verse references when possible."
    )

    @property
    def categories(self) -> tuple[str, str, str]:
        return (
            self.category_factual,
            self.category_emotional,
            self.category_creative,
        )

    @model_validator(mode="after")
    def _resolve_vectorstore_dir(self) -> "Settings":
        if self.chroma_persist_dir is None:
            self.chroma_persist_dir = get_vectorstore_persist_directory(
                embedding_provider=self.embedding_provider,
                embedding_model=self.embedding_model,
                collection_name=self.collection_name,
                root_dir=self.vectorstore_root_dir,
            )
        else:
            self.chroma_persist_dir = self.chroma_persist_dir.expanduser().resolve()

        self.vectorstore_root_dir = self.vectorstore_root_dir.expanduser().resolve()
        return self


settings = Settings()
