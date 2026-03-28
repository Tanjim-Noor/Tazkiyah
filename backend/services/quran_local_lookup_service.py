from __future__ import annotations

import json
import logging
from pathlib import Path

from backend.config import Settings

logger = logging.getLogger(__name__)


class QuranLocalLookupService:
    """Local verse lookup service backed by raw Quran JSON files."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._verse_map: dict[str, dict] = {}
        self._surah_names: dict[int, str] = {}
        self._load()

    def _load_json(self, path: Path) -> dict | list:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _load(self) -> None:
        base_dir = self._settings.quran_raw_data_dir
        surah_meta_path = base_dir / "surah.json"
        surah_dir = base_dir / "surah"
        translation_dir = base_dir / "translation" / self._settings.quran_default_translation_language

        if not surah_meta_path.exists() or not surah_dir.exists() or not translation_dir.exists():
            logger.warning(
                "Quran local lookup data is missing. base_dir=%s, translation_language=%s",
                str(base_dir),
                self._settings.quran_default_translation_language,
            )
            return

        surah_meta = self._load_json(surah_meta_path)
        if isinstance(surah_meta, list):
            for item in surah_meta:
                if not isinstance(item, dict):
                    continue
                try:
                    surah_number = int(item.get("index", "0"))
                except ValueError:
                    continue
                if surah_number > 0:
                    self._surah_names[surah_number] = str(item.get("title", f"Surah {surah_number}"))

        loaded_count = 0
        for surah_number in range(1, 115):
            surah_file = surah_dir / f"surah_{surah_number}.json"
            translation_file = (
                translation_dir
                / f"{self._settings.quran_default_translation_language}_translation_{surah_number}.json"
            )

            if not surah_file.exists() or not translation_file.exists():
                continue

            surah_payload = self._load_json(surah_file)
            translation_payload = self._load_json(translation_file)

            if not isinstance(surah_payload, dict) or not isinstance(translation_payload, dict):
                continue

            surah_verses = surah_payload.get("verse", {})
            translation_verses = translation_payload.get("verse", {})

            if not isinstance(surah_verses, dict) or not isinstance(translation_verses, dict):
                continue

            surah_name = self._surah_names.get(surah_number) or str(surah_payload.get("name", f"Surah {surah_number}"))

            # Intentionally skip verse_0 so lookups remain normalized to chapter:verse.
            for key, arabic_text in surah_verses.items():
                if not key.startswith("verse_"):
                    continue
                try:
                    verse_number = int(key.split("_", maxsplit=1)[1])
                except (IndexError, ValueError):
                    continue

                if verse_number <= 0:
                    continue

                verse_key = f"{surah_number}:{verse_number}"
                translation_text = translation_verses.get(key)

                self._verse_map[verse_key] = {
                    "verse_key": verse_key,
                    "verse_id": verse_key,
                    "surah_name": surah_name,
                    "surah_number": surah_number,
                    "verse_number": verse_number,
                    "arabic_text": arabic_text if isinstance(arabic_text, str) else None,
                    "translation": translation_text if isinstance(translation_text, str) else None,
                }
                loaded_count += 1

        logger.info(
            "Loaded local Quran lookup map with %s verses from %s",
            loaded_count,
            str(base_dir),
        )

    def get_verse(self, verse_key: str) -> dict | None:
        return self._verse_map.get(verse_key)
