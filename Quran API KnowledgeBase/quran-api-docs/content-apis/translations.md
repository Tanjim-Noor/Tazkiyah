# Translations API

> Quran translations in multiple languages  
> **Base Path:** `/resources/translations`, `/quran/translations`

---

## Endpoints Overview

| Endpoint | Description |
|----------|-------------|
| `GET /resources/translations` | List available translations |
| `GET /quran/translations/{translation_id}` | Get single translation text |
| `GET /resources/translations/{id}/by_chapter/{chapter}` | Translation by chapter |
| `GET /resources/translations/{id}/by_juz/{juz}` | Translation by Juz |
| `GET /resources/translations/{id}/by_hizb/{hizb}` | Translation by Hizb |
| `GET /resources/translations/{id}/by_ruku/{ruku}` | Translation by Ruku |

---

## List Available Translations

Get all available translation resources.

```
GET /resources/translations
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | Filter by language code |

**Response (200):**

```json
{
  "translations": [
    {
      "id": 131,
      "name": "Sahih International",
      "author_name": "Saheeh International",
      "slug": "sahih-international",
      "language_name": "english",
      "translated_name": {
        "name": "Sahih International",
        "language_name": "english"
      }
    },
    {
      "id": 85,
      "name": "Abdel Haleem",
      "author_name": "M.A.S. Abdel Haleem",
      "slug": "abdel-haleem",
      "language_name": "english"
    }
  ]
}
```

---

## Get Single Translation

Retrieve translation text for the entire Quran or paginated portions.

```
GET /quran/translations/{translation_id}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `translation_id` | integer | ✓ | Translation resource ID |

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
    },
    {
      "resource_id": 131,
      "text": "[All] praise is [due] to Allah, Lord of the worlds -"
    }
  ],
  "meta": {
    "translation_name": "Sahih International",
    "author_name": "Saheeh International"
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

## Get Translation by Chapter

```
GET /resources/translations/{translation_id}/by_chapter/{chapter_number}
```

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `translation_id` | integer | ✓ | Translation ID |
| `chapter_number` | integer | ✓ | Chapter (1-114) |

---

## Get Translation by Juz

```
GET /resources/translations/{translation_id}/by_juz/{juz_number}
```

---

## Get Translation by Hizb

```
GET /resources/translations/{translation_id}/by_hizb/{hizb_number}
```

---

## Get Translation by Ruku

```
GET /resources/translations/{translation_id}/by_ruku/{ruku_number}
```

---

## Popular Translation IDs

| ID | Name | Language |
|----|------|----------|
| 131 | Sahih International | English |
| 85 | Abdel Haleem | English |
| 20 | Pickthall | English |
| 22 | Yusuf Ali | English |
| 161 | Hilali & Khan | English |
| 203 | King Fahad Complex | Arabic |
| 234 | Mehandipur Qadri | Urdu |

---

## Including Translations with Verses

When fetching verses, include translations using the `translations` parameter:

```bash
# Single translation
curl "/verses/by_chapter/1?translations=131"

# Multiple translations
curl "/verses/by_chapter/1?translations=131,85,20"
```

**Response includes:**

```json
{
  "verses": [
    {
      "verse_key": "1:1",
      "translations": [
        {
          "resource_id": 131,
          "text": "In the name of Allah, the Entirely Merciful..."
        },
        {
          "resource_id": 85,
          "text": "In the name of God, the Lord of Mercy..."
        }
      ]
    }
  ]
}
```

---

## Examples

### List English Translations

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/translations?language=en"
```

### Get Sahih International Translation

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/quran/translations/131"
```

### Get Translation for Al-Fatihah

```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/resources/translations/131/by_chapter/1"
```

---

*[Back to Content APIs](README.md) | [Back to Main Index](../README.md)*
