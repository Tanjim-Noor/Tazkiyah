from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=20)
    temperature: float | None = Field(default=None, ge=0.0, le=2.0)
    return_sources: bool = True


class SourceItem(BaseModel):
    verse_id: str
    surah_name: str | None = None
    surah_number: int | None = None
    verse_number: int | None = None
    score: float | None = None


class ChatFinalPayload(BaseModel):
    answer: str
    category: str
    sources: list[SourceItem]
