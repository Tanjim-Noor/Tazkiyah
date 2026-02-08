#!/usr/bin/env python3
"""
Tazkiyah RAG v2 - Data Loader

Loads quran_full_rag_v2.json and converts verses into LangChain Documents.

Strategy:
  - page_content = translation_clean + commentary_clean (the RAG-searchable text)
  - metadata = surah_number, surah_name, verse_number, id, etc. (for filtering/display)
  - Excludes: footnotes, has_commentary, has_footnotes, commentary_annotated, translation_annotated
"""
import json
import logging
from pathlib import Path
from typing import Optional

from langchain_core.documents import Document

from rag_v2 import config

logger = logging.getLogger(__name__)


def load_quran_json(filepath: Optional[Path] = None) -> dict:
    """Load the quran_full_rag_v2.json file."""
    filepath = filepath or config.DATA_FILE
    logger.info(f"Loading Quran data from: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_surahs = len(data.get("surahs", []))
    total_verses = sum(len(s.get("verses", [])) for s in data.get("surahs", []))
    logger.info(f"Loaded {total_surahs} surahs, {total_verses} verses")
    return data


def create_documents_from_json(
    data: dict,
    include_commentary: bool = True,
    max_content_length: int = 3000,  # Max chars per document for embedding model
) -> list[Document]:
    """
    Convert quran_full_rag_v2.json into LangChain Documents.

    Each verse becomes one Document:
      page_content = translation_clean (+ commentary_clean if available)
      metadata = identifiers and surah info (NO footnotes/annotated fields)

    Args:
        data: Loaded JSON data
        include_commentary: Include commentary in indexed text
        max_content_length: Max characters per document (exceeds embedding model limits)
                           Long content is truncated, with "..." suffix
    """
    documents = []
    skipped_long = 0

    for surah in data.get("surahs", []):
        surah_number = surah.get("surah_number", 0)
        surah_name = surah.get("surah_name", "")
        surah_name_english = surah.get("surah_name_english", "")
        verse_count = surah.get("verse_count", 0)

        for verse in surah.get("verses", []):
            verse_id = verse.get("id", "")
            verse_number = verse.get("verse_number", 0)
            translation_clean = verse.get("translation_clean", "")
            commentary_clean = verse.get("commentary_clean", "")

            # Build page_content: translation + commentary (the searchable text)
            content_parts = []

            # Always include translation
            if translation_clean:
                content_parts.append(
                    f"[Verse {verse_id}] Translation:\n{translation_clean}"
                )

            # Include commentary if present and enabled
            if include_commentary and commentary_clean:
                content_parts.append(f"Commentary:\n{commentary_clean}")

            page_content = "\n\n".join(content_parts)

            if not page_content.strip():
                logger.debug(f"Skipping empty verse: {verse_id}")
                continue

            # Truncate if too long (for embedding model limits)
            if len(page_content) > max_content_length:
                page_content = page_content[:max_content_length - 3] + "..."
                skipped_long += 1

            # Build metadata (only structural/identification fields)
            metadata = {
                "verse_id": verse_id,
                "verse_key": verse_id,
                "surah_number": surah_number,
                "surah_name": surah_name,
                "surah_name_english": surah_name_english,
                "verse_number": verse_number,
                "verse_count": verse_count,
                "type": verse.get("type", "verse"),
                "source": "quran_full_rag_v2.json",
            }

            documents.append(Document(
                page_content=page_content,
                metadata=metadata,
            ))

    logger.info(f"Created {len(documents)} documents from Quran data")
    if skipped_long > 0:
        logger.info(f"  (Truncated {skipped_long} documents that exceeded {max_content_length} chars)")
    return documents


def load_and_create_documents(
    filepath: Optional[Path] = None,
    include_commentary: bool = True,
) -> list[Document]:
    """Convenience: load JSON + create documents in one call."""
    data = load_quran_json(filepath)
    return create_documents_from_json(data, include_commentary=include_commentary)
