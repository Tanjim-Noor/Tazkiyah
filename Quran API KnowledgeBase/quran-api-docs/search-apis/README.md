# Search APIs (v1.0)

> Full-text search across Quran content  
> **Base URL:** `https://apis-prelive.quran.foundation/api/v1`

---

## Overview

The Search API allows searching across verses, chapters, juz, and pages. Requires authentication with the `search` scope.

---

## Authentication

```
x-auth-token: <JWT access token>
x-client-id: <Your client ID>
```

Required scope: `search`

---

## Search Quran Content

```
GET /search
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | ✓ | Search query text |
| `size` | integer | | Results per page (default: 20) |
| `page` | integer | | Page number |
| `language` | string | | Language code for results |

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `x-auth-token` | ✓ | JWT access token |
| `x-client-id` | ✓ | Your client ID |

---

## Response (200 OK)

```json
{
  "search": {
    "query": "mercy",
    "total_results": 150,
    "current_page": 1,
    "total_pages": 8,
    "results": [
      {
        "verse_key": "1:1",
        "verse_id": 1,
        "text": "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ",
        "highlighted": "In the name of Allah, the Entirely <em>Merciful</em>, the Especially <em>Merciful</em>.",
        "translations": [
          {
            "resource_id": 131,
            "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful."
          }
        ]
      }
    ]
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Original search query |
| `total_results` | integer | Total matching results |
| `current_page` | integer | Current page number |
| `total_pages` | integer | Total pages available |
| `results` | array | Array of matching verses |

### Result Object

| Field | Type | Description |
|-------|------|-------------|
| `verse_key` | string | Verse identifier (e.g., `2:255`) |
| `verse_id` | integer | Unique verse ID |
| `text` | string | Arabic text |
| `highlighted` | string | Translation with `<em>` highlights |
| `translations` | array | Matching translations |

---

## Error Responses

### 401 Unauthorized

```json
{
  "success": false,
  "message": "The request requires user authentication",
  "type": "unauthorized"
}
```

### 403 Forbidden

```json
{
  "success": false,
  "message": "Insufficient scope for this request",
  "type": "forbidden"
}
```

### 429 Rate Limited

```json
{
  "success": false,
  "message": "Too many requests, please try again later",
  "type": "rate_limit_exceeded"
}
```

---

## Examples

### Basic Search

```bash
curl "https://apis-prelive.quran.foundation/api/v1/search?q=mercy&size=10" \
  -H "x-auth-token: YOUR_TOKEN" \
  -H "x-client-id: YOUR_CLIENT_ID"
```

### Search with Pagination

```bash
curl "https://apis-prelive.quran.foundation/api/v1/search?q=patience&size=20&page=2" \
  -H "x-auth-token: YOUR_TOKEN" \
  -H "x-client-id: YOUR_CLIENT_ID"
```

### Search in Arabic

```bash
curl "https://apis-prelive.quran.foundation/api/v1/search?q=رحمة&language=ar" \
  -H "x-auth-token: YOUR_TOKEN" \
  -H "x-client-id: YOUR_CLIENT_ID"
```

---

## Search Tips

1. **Exact phrases**: Use quotes for exact matching
2. **Arabic text**: Search in Arabic script works
3. **Transliteration**: Common transliterations are supported
4. **Translation search**: Searches across translations in specified language

---

*[Back to Main Index](../README.md)*
