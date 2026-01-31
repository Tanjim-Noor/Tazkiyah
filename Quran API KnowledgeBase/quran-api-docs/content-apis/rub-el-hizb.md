# Rub El Hizb API

> 240 quarter-Hizb segments for fine-grained reading  
> **Base Path:** `/verses/by_rub_el_hizb`

---

## Overview

Each Hizb is divided into 4 Rub (quarters), creating 240 total segments. These are marked in printed Mushafs with ۞ symbols. Rub El Hizb provides the finest standard division for reading schedules.

---

## Endpoints

### Get Verses by Rub El Hizb

Retrieve all verses within a specific Rub El Hizb segment.

```
GET /verses/by_rub_el_hizb/{rub_el_hizb_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `rub_el_hizb_number` | integer | ✓ | 1-240 | Rub El Hizb number |

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
    "total_pages": 2,
    "total_records": 18
  }
}
```

---

## Division Hierarchy

```
Quran
├── 30 Juz
│   ├── 60 Hizb (2 per Juz)
│   │   ├── 240 Rub El Hizb (4 per Hizb)
```

| Level | Count | Relationship |
|-------|-------|--------------|
| Juz | 30 | Base division |
| Hizb | 60 | 2 per Juz |
| Rub El Hizb | 240 | 4 per Hizb, 8 per Juz |

**Formula:** 
- `Hizb = ceil(Rub El Hizb / 4)`
- `Juz = ceil(Rub El Hizb / 8)`

---

## Examples

### Get First Rub El Hizb

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_rub_el_hizb/1"
```

### Get Rub with Translation

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_rub_el_hizb/17?translations=131"
```

### Get Last Rub El Hizb

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_rub_el_hizb/240?audio=7"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
