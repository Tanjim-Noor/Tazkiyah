# Ruku API

> Thematic paragraph groupings (~556 sections)  
> **Base Path:** `/resources/translations/{id}/by_ruku`

---

## Overview

Ruku (plural: Ruku'at) are thematic divisions used primarily in the Indo-Pakistani tradition. They group verses by topic or subject matter, making them useful for study and topical reading. There are approximately 556 Ruku across the Quran.

---

## Endpoints

### Get Translations by Ruku

Retrieve translation text for verses within a specific Ruku.

```
GET /resources/translations/{translation_id}/by_ruku/{ruku_number}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `translation_id` | integer | ✓ | Translation resource ID |
| `ruku_number` | integer | ✓ | Ruku number (1-~556) |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `per_page` | integer | Results per page |
| `page` | integer | Page number |

**Response (200):**

```json
{
  "translations": [
    {
      "resource_id": 131,
      "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful."
    }
  ],
  "meta": {
    "translation_name": "Sahih International",
    "author_name": "Saheeh International"
  },
  "pagination": {
    "per_page": 10,
    "current_page": 1,
    "next_page": 2,
    "total_pages": 2,
    "total_records": 15
  }
}
```

---

## Ruku Characteristics

| Aspect | Description |
|--------|-------------|
| Count | ~556 across Quran |
| Purpose | Thematic/topical groupings |
| Tradition | Primarily Indo-Pakistani |
| Marking | ع symbol in printed Mushafs |

---

## Verse Object with Ruku

When retrieving verses, the `ruku_number` field indicates which Ruku the verse belongs to:

```json
{
  "verse": {
    "id": 262,
    "verse_key": "2:255",
    "ruku_number": 35,
    ...
  }
}
```

---

## Examples

### Get First Ruku Translation

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/translations/131/by_ruku/1"
```

### Get Ruku 35 (Contains Ayat al-Kursi)

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/translations/131/by_ruku/35"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
