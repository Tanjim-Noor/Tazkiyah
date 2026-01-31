# Hizb API

> 60-part division of the Quran (half-Juz segments)  
> **Base Path:** `/verses/by_hizb`

---

## Overview

Each Juz is divided into 2 Hizb, creating 60 total Hizb divisions. This provides finer granularity for reading schedules.

---

## Endpoints

### Get Verses by Hizb

Retrieve all verses within a specific Hizb.

```
GET /verses/by_hizb/{hizb_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `hizb_number` | integer | ✓ | 1-60 | Hizb number |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | ISO language code |
| `words` | boolean | Include word breakdown |
| `translations` | string | Translation IDs |
| `audio` | integer | Recitation ID |
| `tafsirs` | string | Tafsir IDs |
| `per_page` | integer | Results per page (max 50) |
| `page` | integer | Page number |

**Response (200):**

```json
{
  "verses": [
    {
      "id": 1,
      "verse_number": 1,
      "verse_key": "1:1",
      "juz_number": 1,
      "hizb_number": 1,
      "rub_el_hizb_number": 1,
      "page_number": 1,
      ...
    }
  ],
  "pagination": {
    "per_page": 10,
    "current_page": 1,
    "next_page": 2,
    "total_pages": 8,
    "total_records": 75
  }
}
```

---

### Get Translations by Hizb

Retrieve translations for verses in a Hizb.

```
GET /resources/translations/{translation_id}/by_hizb/{hizb_number}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `translation_id` | integer | ✓ | Translation resource ID |
| `hizb_number` | integer | ✓ | Hizb number (1-60) |

---

## Hizb Relationship

| Juz | Hizb |
|-----|------|
| 1 | 1, 2 |
| 2 | 3, 4 |
| 3 | 5, 6 |
| ... | ... |
| 30 | 59, 60 |

**Formula:** `Hizb = (Juz - 1) * 2 + [1 or 2]`

---

## Examples

### Get First Hizb

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_hizb/1"
```

### Get Hizb with Translation

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_hizb/10?translations=131"
```

### Get Last Hizb with Audio

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_hizb/60?audio=7"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
