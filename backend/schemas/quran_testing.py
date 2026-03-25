from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


IncludeField = Literal[
    "arabic",
    "transliteration",
    "translations",
    "tafsirs",
    "metadata",
    "footnotes",
    "raw",
]


class QuranVerseTestRequest(BaseModel):
    verse_key: str = Field(pattern=r"^\d{1,3}:\d{1,3}$")
    include: list[IncludeField] = Field(
        default_factory=lambda: [
            "arabic",
            "translations",
            "metadata",
        ]
    )
    translation_ids: list[int] = Field(default_factory=list)
    tafsir_ids: list[int] = Field(default_factory=list)
    language: str = Field(default="en", min_length=2, max_length=5)

    @field_validator("include")
    @classmethod
    def ensure_include_not_empty(cls, value: list[IncludeField]) -> list[IncludeField]:
        if not value:
            raise ValueError("At least one include field is required")
        return value

    @field_validator("translation_ids", "tafsir_ids")
    @classmethod
    def ensure_positive_ids(cls, value: list[int]) -> list[int]:
        if any(item <= 0 for item in value):
            raise ValueError("Resource IDs must be positive integers")
        return value


class QuranTranslationItem(BaseModel):
    id: int
    name: str
    language_name: str | None = None
    text: str


class QuranTafsirItem(BaseModel):
    id: int
    name: str
    language_name: str | None = None
    text: str


class QuranFootnoteItem(BaseModel):
    key: str
    text: str


class QuranVerseMetadata(BaseModel):
    surah_number: int
    verse_number: int
    surah_name: str | None = None
    surah_name_arabic: str | None = None
    juz: int | None = None
    page: int | None = None
    hizb: int | None = None
    rub_el_hizb: int | None = None
    ruku: int | None = None
    manzil: int | None = None
    sajdah: int | None = None
    revelation_place: str | None = None
    revelation_order: int | None = None


class QuranVerseData(BaseModel):
    arabic_text: str | None = None
    transliteration: str | None = None
    translations: list[QuranTranslationItem] = Field(default_factory=list)
    tafsirs: list[QuranTafsirItem] = Field(default_factory=list)
    footnotes: list[QuranFootnoteItem] = Field(default_factory=list)
    metadata: QuranVerseMetadata | None = None
    raw: dict[str, Any] | None = None


class QuranVerseTestResponse(BaseModel):
    verse_key: str
    requested_include: list[IncludeField]
    warnings: list[str] = Field(default_factory=list)
    duration_ms: int
    data: QuranVerseData


class QuranResourceItem(BaseModel):
    id: int
    name: str
    language_name: str | None = None
    author_name: str | None = None


class QuranResourcesResponse(BaseModel):
    language: str | None = None
    translations: list[QuranResourceItem] = Field(default_factory=list)
    tafsirs: list[QuranResourceItem] = Field(default_factory=list)
