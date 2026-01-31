# Reading Sessions API

> Track user reading progress  
> **Base Path:** `/api/v1/reading-sessions`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reading-sessions` | Get reading session |
| POST | `/reading-sessions` | Create/update session |

---

## Get Reading Session

Retrieve current reading progress.

```
GET /reading-sessions
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "id": "session123",
    "lastReadVerseKey": "2:255",
    "lastReadPage": 42,
    "lastReadJuz": 3,
    "lastReadChapter": 2,
    "mushafId": 1,
    "updatedAt": "2023-01-21T07:28:13.023Z"
  }
}
```

---

## Create/Update Reading Session

Save reading progress.

```
POST /reading-sessions
Content-Type: application/json
```

### Request Body

```json
{
  "lastReadVerseKey": "2:255",
  "lastReadPage": 42,
  "lastReadJuz": 3,
  "lastReadChapter": 2,
  "mushafId": 1
}
```

| Field | Type | Description |
|-------|------|-------------|
| `lastReadVerseKey` | string | Last verse read (e.g., `2:255`) |
| `lastReadPage` | integer | Page number |
| `lastReadJuz` | integer | Juz number |
| `lastReadChapter` | integer | Chapter number |
| `mushafId` | integer | Mushaf ID (1-19) |

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
