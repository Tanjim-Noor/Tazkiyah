# Juz API

> 30-part equal division of the Quran  
> **Base Path:** `/juzs`

---

## Overview

The Quran is divided into 30 Juz (plural: Ajza) of approximately equal length, designed for reading the entire Quran over a month.

---

## Endpoints

### List All Juzs

Retrieve information about all 30 Juz divisions.

```
GET /juzs
```

**Response (200):**

```json
{
  "juzs": [
    {
      "id": 1,
      "juz_number": 1,
      "verse_mapping": {
        "1": "1-7",
        "2": "1-141"
      },
      "first_verse_id": 1,
      "last_verse_id": 148,
      "verses_count": 148
    },
    {
      "id": 2,
      "juz_number": 2,
      "verse_mapping": {
        "2": "142-252"
      },
      "first_verse_id": 149,
      "last_verse_id": 259,
      "verses_count": 111
    }
  ]
}
```

---

### Get Verses by Juz

Retrieve all verses within a specific Juz.

```
GET /verses/by_juz/{juz_number}
```

**Path Parameters:**

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `juz_number` | integer | ✓ | 1-30 | Juz number |

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
      ...
    }
  ],
  "pagination": {
    "per_page": 10,
    "current_page": 1,
    "next_page": 2,
    "total_pages": 15,
    "total_records": 148
  }
}
```

---

## Juz Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique ID |
| `juz_number` | integer | Juz number (1-30) |
| `verse_mapping` | object | Chapter to verse range mapping |
| `first_verse_id` | integer | ID of first verse |
| `last_verse_id` | integer | ID of last verse |
| `verses_count` | integer | Total verses in Juz |

---

## Juz Reference Table

| Juz | Starts | Ends | Verses |
|-----|--------|------|--------|
| 1 | 1:1 | 2:141 | 148 |
| 2 | 2:142 | 2:252 | 111 |
| 3 | 2:253 | 3:92 | 126 |
| 4 | 3:93 | 4:23 | 131 |
| 5 | 4:24 | 4:147 | 124 |
| ... | ... | ... | ... |
| 30 | 78:1 | 114:6 | 564 |

---

## Examples

### List All Juz Divisions

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/juzs"
```

### Get First Juz with Translations

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_juz/1?translations=131"
```

### Get Last Juz (Juz Amma) with Audio

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_juz/30?audio=7"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
