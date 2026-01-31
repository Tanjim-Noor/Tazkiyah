# Content APIs (v4)

> Non-user-specific resources for Quran data access  
> **Base URL:** `https://apis-prelive.quran.foundation/content/api/v4`

---

## Overview

Content APIs provide access to Quran text, translations, tafsirs (exegesis), audio recitations, and metadata. These endpoints do not require authentication and focus on non-user-specific resources.

---

## API Sections

| Section | Description | File |
|---------|-------------|------|
| Audio | Recitations and audio files | [audio.md](audio.md) |
| Chapters | Surah metadata and information | [chapters.md](chapters.md) |
| Verses | Ayah retrieval methods | [verses.md](verses.md) |
| Juz | 30-part Quran division | [juz.md](juz.md) |
| Hizb | 60-part division (half-Juz) | [hizb.md](hizb.md) |
| Rub El Hizb | 240 quarter-Hizb segments | [rub-el-hizb.md](rub-el-hizb.md) |
| Ruku | Thematic paragraph groupings | [ruku.md](ruku.md) |
| Manzil | 7-day reading division | [manzil.md](manzil.md) |
| Translations | Translation resources | [translations.md](translations.md) |
| Tafsirs | Commentary/exegesis | [tafsirs.md](tafsirs.md) |
| Resources | Languages, scripts, reciters | [resources.md](resources.md) |
| Quran | Direct text retrieval | [quran.md](quran.md) |

---

## Common Query Parameters

Most verse-related endpoints support these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | ISO language code (e.g., `en`, `ar`, `ur`) |
| `words` | boolean | Include word-by-word breakdown |
| `translations` | string | Comma-separated translation IDs |
| `audio` | integer | Recitation ID for audio URLs |
| `tafsirs` | string | Comma-separated tafsir IDs |
| `fields` | string | Verse fields to include |
| `word_fields` | string | Word-level fields to include |
| `translation_fields` | string | Translation fields to include |
| `per_page` | integer | Results per page (max 50) |
| `page` | integer | Page number |

---

## Field References

For detailed field options, see the official documentation:
- **Verse Fields:** `/docs/api/field-reference#verse-fields`
- **Word Fields:** `/docs/api/field-reference#word-fields`
- **Translation Fields:** `/docs/api/field-reference#translation-fields`
- **Tafsir Fields:** `/docs/api/field-reference#tafsir-fields`

---

## Pagination

All list endpoints return pagination metadata:

```json
{
  "pagination": {
    "per_page": 10,
    "current_page": 1,
    "next_page": 2,
    "total_pages": 29,
    "total_records": 286
  }
}
```

---

## Quran Divisions Reference

| Division | Count | Description |
|----------|-------|-------------|
| Chapters (Surah) | 114 | Primary divisions |
| Juz | 30 | Equal reading portions |
| Hizb | 60 | Half-Juz segments |
| Rub El Hizb | 240 | Quarter-Hizb markers |
| Manzil | 7 | Weekly reading plan |
| Ruku | ~556 | Thematic paragraphs |

---

## Mushaf Types

| ID | Name | Description |
|----|------|-------------|
| 1 | QCFV2 | Quran Complex Font v2 |
| 2 | QCFV1 | Quran Complex Font v1 |
| 3 | Indopak | Indo-Pakistani script |
| 4 | UthmaniHafs | Uthmani Hafs script |
| 5 | KFGQPCHAFS | King Fahd Complex Hafs |
| 6 | Indopak15Lines | Indopak 15-line |
| 7 | Indopak16Lines | Indopak 16-line |
| 11 | Tajweed | Color-coded Tajweed |
| 19 | QCFTajweedV4 | QCF Tajweed v4 |

---

*[Back to Main Index](../README.md)*
