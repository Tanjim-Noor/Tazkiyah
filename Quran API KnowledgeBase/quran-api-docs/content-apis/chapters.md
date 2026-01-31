# Chapters API

> Retrieve Surah (chapter) metadata and information  
> **Base Path:** `/chapters`

---

## Endpoints

### List All Chapters

Retrieve all 114 chapters with metadata.

```
GET /chapters
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Language for translated names (default: `en`) |

**Response (200):**

```json
{
  "chapters": [
    {
      "id": 1,
      "revelation_place": "makkah",
      "revelation_order": 5,
      "bismillah_pre": false,
      "name_simple": "Al-Fatihah",
      "name_complex": "Al-Fātiĥah",
      "name_arabic": "الفاتحة",
      "verses_count": 7,
      "pages": [1, 1],
      "translated_name": {
        "language_name": "english",
        "name": "The Opener"
      }
    }
  ]
}
```

---

### Get Chapter by ID

Retrieve a specific chapter by its number (1-114).

```
GET /chapters/{id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | ✓ | Chapter number (1-114) |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Language for translated name |

**Response (200):**

```json
{
  "chapter": {
    "id": 1,
    "revelation_place": "makkah",
    "revelation_order": 5,
    "bismillah_pre": false,
    "name_simple": "Al-Fatihah",
    "name_complex": "Al-Fātiĥah",
    "name_arabic": "الفاتحة",
    "verses_count": 7,
    "pages": [1, 1],
    "translated_name": {
      "language_name": "english",
      "name": "The Opener"
    }
  }
}
```

---

### Get Chapter Info

Retrieve detailed information about a chapter including description and summary.

```
GET /chapters/{chapter_id}/info
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chapter_id` | integer | ✓ | Chapter number (1-114) |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Language for chapter info |

**Response (200):**

```json
{
  "chapter_info": {
    "id": 1,
    "chapter_id": 1,
    "language_name": "english",
    "short_text": "Brief description...",
    "source": "Source attribution",
    "text": "Full chapter description and context..."
  }
}
```

---

## Chapter Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Chapter number (1-114) |
| `revelation_place` | string | `makkah` or `madinah` |
| `revelation_order` | integer | Chronological revelation order |
| `bismillah_pre` | boolean | Whether Bismillah appears before first verse |
| `name_simple` | string | Simplified transliteration |
| `name_complex` | string | Complex transliteration with diacritics |
| `name_arabic` | string | Arabic name |
| `verses_count` | integer | Number of verses |
| `pages` | array | Start and end page numbers [start, end] |
| `translated_name` | object | Translation of chapter name |

---

## Examples

### Get All Chapters in Arabic

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/chapters?language=ar"
```

### Get Surah Al-Baqarah

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/chapters/2"
```

### Get Info for Surah Yasin

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/chapters/36/info?language=en"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
