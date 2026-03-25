from __future__ import annotations

import re
import time
from typing import Any

from fastapi import HTTPException

from backend.schemas.quran_testing import QuranVerseTestRequest
from tools.python.collection.quran_api import QuranAPIClient

FOOTNOTE_PATTERN = re.compile(r"<sup\s+foot_note=(\d+)>(\d+)</sup>")
TAG_PATTERN = re.compile(r"<[^>]+>")


class QuranAPITestingService:
    def __init__(self, rate_limit_delay: float = 0.3):
        self.client = QuranAPIClient(rate_limit_delay=rate_limit_delay)

    def close(self) -> None:
        self.client.close()

    @staticmethod
    def _strip_html(text: str) -> str:
        return TAG_PATTERN.sub("", text).strip()

    @staticmethod
    def _parse_verse_key(verse_key: str) -> tuple[int, int]:
        try:
            surah_raw, verse_raw = verse_key.split(":", maxsplit=1)
            surah_number = int(surah_raw)
            verse_number = int(verse_raw)
            if surah_number < 1 or surah_number > 114:
                raise ValueError("Surah number must be between 1 and 114")
            if verse_number < 1:
                raise ValueError("Verse number must be greater than 0")
            return surah_number, verse_number
        except ValueError as exc:
            raise HTTPException(status_code=422, detail={"message": str(exc)}) from exc

    def _find_verse(self, surah_number: int, verse_number: int, translation_ids: list[int]) -> dict[str, Any]:
        verses = self.client.get_all_verses_by_chapter(
            chapter_number=surah_number,
            translations=translation_ids or None,
            fields=["text_uthmani"],
        )
        verse = next((item for item in verses if item.get("verse_number") == verse_number), None)
        if verse is None:
            raise HTTPException(
                status_code=404,
                detail={"message": f"Verse {surah_number}:{verse_number} was not found"},
            )
        return verse

    def _resource_name_map(self, items: list[dict[str, Any]]) -> dict[int, dict[str, str | None]]:
        return {
            int(item["id"]): {
                "name": item.get("name", f"Resource {item['id']}"),
                "language_name": item.get("language_name"),
            }
            for item in items
            if "id" in item
        }

    def resources(self, language: str | None) -> dict[str, Any]:
        translations = self.client.get_translations_list(language=language or None)
        tafsirs = self.client.get_tafsirs_list(language=language or None)
        return {
            "language": language or None,
            "translations": [
                {
                    "id": int(item["id"]),
                    "name": item.get("name", f"Translation {item['id']}"),
                    "language_name": item.get("language_name"),
                    "author_name": item.get("author_name"),
                }
                for item in translations
                if "id" in item
            ],
            "tafsirs": [
                {
                    "id": int(item["id"]),
                    "name": item.get("name", f"Tafsir {item['id']}"),
                    "language_name": item.get("language_name"),
                    "author_name": item.get("author_name"),
                }
                for item in tafsirs
                if "id" in item
            ],
        }

    def verse_details(self, payload: QuranVerseTestRequest) -> dict[str, Any]:
        started = time.perf_counter()
        warnings: list[str] = []

        surah_number, verse_number = self._parse_verse_key(payload.verse_key)
        chapter = self.client.get_chapter(chapter_number=surah_number, language=payload.language)
        verse = self._find_verse(surah_number, verse_number, payload.translation_ids)

        include_set = set(payload.include)
        translation_resources = self.client.get_translations_list(language=payload.language or None)
        tafsir_resources = self.client.get_tafsirs_list(language=payload.language or None)
        translation_resource_map = self._resource_name_map(translation_resources)
        tafsir_resource_map = self._resource_name_map(tafsir_resources)

        result: dict[str, Any] = {
            "arabic_text": None,
            "transliteration": None,
            "translations": [],
            "tafsirs": [],
            "footnotes": [],
            "metadata": None,
            "raw": None,
        }

        if "arabic" in include_set:
            result["arabic_text"] = verse.get("text_uthmani")

        if "transliteration" in include_set:
            transliteration = verse.get("transliteration")
            if isinstance(transliteration, dict):
                result["transliteration"] = transliteration.get("text")
            elif isinstance(transliteration, str):
                result["transliteration"] = transliteration
            else:
                warnings.append("Transliteration is not available in this verse payload")

        if "translations" in include_set:
            if not payload.translation_ids:
                warnings.append("No translation IDs were provided; translations section is empty")
            for translation in verse.get("translations", []):
                resource_id = int(translation.get("resource_id", 0))
                if payload.translation_ids and resource_id not in payload.translation_ids:
                    continue
                resource_info = translation_resource_map.get(resource_id, {})
                result["translations"].append(
                    {
                        "id": resource_id,
                        "name": resource_info.get("name", f"Translation {resource_id}"),
                        "language_name": resource_info.get("language_name"),
                        "text": self._strip_html(translation.get("text", "")),
                    }
                )

                if "footnotes" in include_set:
                    matches = FOOTNOTE_PATTERN.findall(translation.get("text", ""))
                    if not matches:
                        continue
                    for footnote_id, footnote_number in matches:
                        footnote_payload = self.client.get_footnote(int(footnote_id))
                        if not footnote_payload:
                            continue
                        key = f"{resource_info.get('name', resource_id)}:{footnote_number}"
                        result["footnotes"].append(
                            {
                                "key": key,
                                "text": self._strip_html(footnote_payload.get("text", "")),
                            }
                        )

        if "tafsirs" in include_set:
            if not payload.tafsir_ids:
                warnings.append("No tafsir IDs were provided; tafsirs section is empty")
            for tafsir_id in payload.tafsir_ids:
                try:
                    tafsir = self.client.get_tafsir_by_ayah(tafsir_id=tafsir_id, verse_key=payload.verse_key)
                    if not tafsir:
                        warnings.append(f"Tafsir {tafsir_id} is not available for verse {payload.verse_key}")
                        continue
                    resource_info = tafsir_resource_map.get(tafsir_id, {})
                    result["tafsirs"].append(
                        {
                            "id": tafsir_id,
                            "name": resource_info.get("name", f"Tafsir {tafsir_id}"),
                            "language_name": resource_info.get("language_name"),
                            "text": self._strip_html(tafsir.get("text", "")),
                        }
                    )
                except Exception:
                    warnings.append(f"Failed to fetch tafsir {tafsir_id}")

        if "metadata" in include_set:
            result["metadata"] = {
                "surah_number": surah_number,
                "verse_number": verse_number,
                "surah_name": chapter.get("name_simple"),
                "surah_name_arabic": chapter.get("name_arabic"),
                "juz": verse.get("juz_number"),
                "page": verse.get("page_number"),
                "hizb": verse.get("hizb_number"),
                "rub_el_hizb": verse.get("rub_el_hizb_number"),
                "ruku": verse.get("ruku_number"),
                "manzil": verse.get("manzil_number"),
                "sajdah": verse.get("sajdah_number"),
                "revelation_place": chapter.get("revelation_place"),
                "revelation_order": chapter.get("revelation_order"),
            }

        if "raw" in include_set:
            result["raw"] = {
                "chapter": chapter,
                "verse": verse,
            }

        duration_ms = int((time.perf_counter() - started) * 1000)
        return {
            "verse_key": payload.verse_key,
            "requested_include": payload.include,
            "warnings": warnings,
            "duration_ms": duration_ms,
            "data": result,
        }
