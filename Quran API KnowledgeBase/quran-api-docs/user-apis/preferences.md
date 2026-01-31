# Preferences API

> User settings and preferences  
> **Base Path:** `/api/v1/preferences`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/preferences` | Get user preferences |
| POST | `/preferences` | Create/update preferences |
| DELETE | `/preferences` | Reset preferences |

---

## Get Preferences

Retrieve current user preferences.

```
GET /preferences
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "id": "pref123",
    "translationIds": [131, 85],
    "tafsirId": 169,
    "reciterId": 7,
    "mushafId": 1,
    "fontSize": 24,
    "wordByWord": true,
    "autoScroll": false,
    "readingMode": "translation"
  }
}
```

---

## Create/Update Preferences

Set user preferences.

```
POST /preferences
Content-Type: application/json
```

### Request Body

```json
{
  "translationIds": [131, 85],
  "tafsirId": 169,
  "reciterId": 7,
  "mushafId": 1,
  "fontSize": 24,
  "wordByWord": true,
  "autoScroll": false,
  "readingMode": "translation"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `translationIds` | integer[] | Preferred translation IDs |
| `tafsirId` | integer | Default tafsir ID |
| `reciterId` | integer | Default reciter ID |
| `mushafId` | integer | Default Mushaf (1-19) |
| `fontSize` | integer | Text size preference |
| `wordByWord` | boolean | Show word-by-word |
| `autoScroll` | boolean | Auto-scroll with audio |
| `readingMode` | string | Display mode |

---

## Reset Preferences

Reset to defaults.

```
DELETE /preferences
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
