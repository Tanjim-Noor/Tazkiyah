from __future__ import annotations

from pydantic import BaseModel


class ConfigResponse(BaseModel):
    app_name: str
    environment: str
    llm_provider: str
    embedding_provider: str
    vectorstore_provider: str
    llm_model: str
    embedding_model: str
    collection_name: str
    top_k: int
    categories: list[str]
    langsmith_tracing: bool
    langsmith_project: str
    vector_count: int
