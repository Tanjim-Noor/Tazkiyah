# Tafsirs API

> Quranic exegesis and commentary resources  
> **Base Path:** `/resources/tafsirs`, `/quran/tafsirs`

---

## Overview

Tafsir (plural: Tafasir) refers to scholarly commentary and interpretation of Quranic verses. The API provides access to multiple tafsir sources.

---

## Endpoints

### List Available Tafsirs

Get all available tafsir resources.

```
GET /resources/tafsirs
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Filter by language code |

**Response (200):**

```json
{
  "tafsirs": [
    {
      "id": 169,
      "name": "Tafsir Ibn Kathir",
      "author_name": "Ibn Kathir",
      "slug": "tafsir-ibn-kathir",
      "language_name": "english",
      "translated_name": {
        "name": "Tafsir Ibn Kathir",
        "language_name": "english"
      }
    },
    {
      "id": 93,
      "name": "Tafsir al-Jalalayn",
      "author_name": "Jalal ad-Din al-Mahalli and Jalal ad-Din as-Suyuti",
      "slug": "tafsir-al-jalalayn",
      "language_name": "arabic"
    }
  ]
}
```

---

### Get Tafsir by ID

Retrieve tafsir content for the entire Quran or paginated.

```
GET /quran/tafsirs/{tafsir_id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tafsir_id` | integer | ✓ | Tafsir resource ID |

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `per_page` | integer | Results per page |
| `page` | integer | Page number |

**Response (200):**

```json
{
  "tafsirs": [
    {
      "resource_id": 169,
      "text": "<p>Commentary on this verse...</p>",
      "verse_id": 1,
      "verse_key": "1:1"
    }
  ],
  "meta": {
    "tafsir_name": "Tafsir Ibn Kathir",
    "author_name": "Ibn Kathir"
  },
  "pagination": {
    "per_page": 50,
    "current_page": 1,
    "next_page": 2,
    "total_pages": 125,
    "total_records": 6236
  }
}
```

---

## Including Tafsirs with Verses

When fetching verses, include tafsir using the `tafsirs` parameter:

```bash
# Single tafsir
curl "/verses/by_key/2:255?tafsirs=169"

# Multiple tafsirs
curl "/verses/by_key/2:255?tafsirs=169,93"
```

**Response includes:**

```json
{
  "verse": {
    "verse_key": "2:255",
    "tafsirs": [
      {
        "resource_id": 169,
        "text": "<p>This is Ayat al-Kursi. Ibn Kathir says...</p>"
      }
    ]
  }
}
```

---

## Popular Tafsir IDs

| ID | Name | Language | Author |
|----|------|----------|--------|
| 169 | Tafsir Ibn Kathir | English | Ibn Kathir |
| 93 | Tafsir al-Jalalayn | Arabic | Al-Mahalli & As-Suyuti |
| 168 | Tafsir as-Saadi | Arabic | Abdur Rahman as-Saadi |
| 91 | Maariful Quran | English | Mufti Muhammad Shafi |

---

## Examples

### List All Tafsirs

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/tafsirs"
```

### Get English Tafsirs

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/tafsirs?language=en"
```

### Get Tafsir for Ayat al-Kursi

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_key/2:255?tafsirs=169"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
