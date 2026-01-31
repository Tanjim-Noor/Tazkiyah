# Verses API

> Retrieve Ayat (verses) by various division methods  
> **Base Path:** `/verses`

---

## Endpoints Overview

| Endpoint | Description |
|----------|-------------|
| `GET /verses/by_chapter/{chapter_number}` | Get verses by chapter |
| `GET /verses/by_page/{page_number}` | Get verses by page |
| `GET /verses/by_juz/{juz_number}` | Get verses by Juz |
| `GET /verses/by_hizb/{hizb_number}` | Get verses by Hizb |
| `GET /verses/by_rub_el_hizb/{rub_el_hizb_number}` | Get verses by Rub El Hizb |
| `GET /verses/by_key/{verse_key}` | Get single verse by key |
| `GET /verses/random` | Get a random verse |

---

## Common Query Parameters

All verse endpoints support these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | ISO language code (default: `en`) |
| `words` | boolean | Include word-by-word breakdown |
| `translations` | string | Comma-separated translation IDs (e.g., `131,85`) |
| `audio` | integer | Recitation ID for audio URLs |
| `tafsirs` | string | Comma-separated tafsir IDs |
| `fields` | string | Verse fields to include |
| `word_fields` | string | Word-level fields |
| `translation_fields` | string | Translation fields |
| `per_page` | integer | Results per page (max 50, default 10) |
| `page` | integer | Page number |

---

## Get Verses by Chapter

Retrieve all verses in a specific chapter with pagination.

```
GET /verses/by_chapter/{chapter_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `chapter_number` | integer | ✓ | 1-114 | Chapter number |

**Response (200):**

```json
{
  "verses": [
    {
      "id": 1,
      "verse_number": 1,
      "verse_key": "1:1",
      "hizb_number": 1,
      "rub_el_hizb_number": 1,
      "ruku_number": 1,
      "manzil_number": 1,
      "sajdah_number": null,
      "page_number": 1,
      "juz_number": 1,
      "words": [...],
      "translations": [...]
    }
  ],
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

## Get Verses by Page

Retrieve verses on a specific Mushaf page.

```
GET /verses/by_page/{page_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `page_number` | integer | ✓ | 1-604 | Page number |

---

## Get Verses by Juz

Retrieve verses in a specific Juz (30 equal parts).

```
GET /verses/by_juz/{juz_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `juz_number` | integer | ✓ | 1-30 | Juz number |

---

## Get Verses by Hizb

Retrieve verses in a specific Hizb (60 parts, half-Juz).

```
GET /verses/by_hizb/{hizb_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `hizb_number` | integer | ✓ | 1-60 | Hizb number |

---

## Get Verses by Rub El Hizb

Retrieve verses in a Rub El Hizb (240 quarter-Hizb segments).

```
GET /verses/by_rub_el_hizb/{rub_el_hizb_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `rub_el_hizb_number` | integer | ✓ | 1-240 | Rub El Hizb number |

---

## Get Single Verse by Key

Retrieve a specific verse using its unique key.

```
GET /verses/by_key/{verse_key}
```

**Path Parameters:**

| Parameter | Type | Required | Format | Description |
|-----------|------|----------|--------|-------------|
| `verse_key` | string | ✓ | `{chapter}:{verse}` | Verse key (e.g., `2:255`) |

**Response (200):**

```json
{
  "verse": {
    "id": 262,
    "verse_number": 255,
    "verse_key": "2:255",
    "hizb_number": 5,
    "rub_el_hizb_number": 17,
    "ruku_number": 35,
    "manzil_number": 1,
    "sajdah_number": null,
    "page_number": 42,
    "juz_number": 3,
    "text_uthmani": "ٱللَّهُ لَآ إِلَـٰهَ إِلَّا هُوَ...",
    "words": [...],
    "translations": [...]
  }
}
```

---

## Get Random Verse

Retrieve a random verse from the Quran.

```
GET /verses/random
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Language for translations |
| `translations` | string | Translation IDs |
| `audio` | integer | Recitation ID |
| `tafsirs` | string | Tafsir IDs |

**Response (200):**

```json
{
  "verse": {
    "id": 3489,
    "verse_number": 18,
    "verse_key": "29:18",
    "chapter_id": 29,
    ...
  }
}
```

---

## Verse Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique verse ID |
| `verse_number` | integer | Verse number within chapter |
| `verse_key` | string | Unique key format `{chapter}:{verse}` |
| `chapter_id` | integer | Chapter number |
| `hizb_number` | integer | Hizb containing this verse |
| `rub_el_hizb_number` | integer | Rub El Hizb number |
| `ruku_number` | integer | Ruku number |
| `manzil_number` | integer | Manzil number (1-7) |
| `sajdah_number` | integer/null | Sajdah prostration number if applicable |
| `page_number` | integer | Mushaf page number |
| `juz_number` | integer | Juz number |
| `text_uthmani` | string | Uthmani script text |
| `text_imlaei` | string | Imlaei script text |
| `text_indopak` | string | Indo-Pakistani script |
| `words` | array | Word-by-word breakdown (if requested) |
| `translations` | array | Translation texts (if requested) |

---

## Examples

### Get Al-Fatihah with English Translation

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_chapter/1?translations=131&language=en"
```

### Get Ayat al-Kursi (2:255) with Words

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_key/2:255?words=true"
```

### Get Random Verse with Audio

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/random?audio=7"
```

### Get First Juz with Multiple Translations

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_juz/1?translations=131,85,20"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
