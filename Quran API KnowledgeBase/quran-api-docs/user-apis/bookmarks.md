# Bookmarks API

> Save and manage verse, page, juz, and surah bookmarks  
> **Base Path:** `/api/v1/bookmarks`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/bookmarks` | Add a bookmark |
| GET | `/bookmarks` | Get all bookmarks |
| GET | `/bookmarks/exists` | Check if bookmark exists |
| DELETE | `/bookmarks` | Delete a bookmark |
| GET | `/bookmarks/collections` | Get bookmark's collections |
| POST | `/bookmarks/sync` | Sync bookmarks |

---

## Add Bookmark

Create a new bookmark.

```
POST /bookmarks
Content-Type: application/json
```

### Request Body (Ayah Bookmark)

```json
{
  "key": 1,
  "type": "ayah",
  "verseNumber": 5,
  "mushaf": 1
}
```

### Request Body (Surah/Juz/Page Bookmark)

```json
{
  "key": 30,
  "type": "juz",
  "mushaf": 1
}
```

### Body Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | integer | ✓ | Surah, Juz, or page number |
| `type` | string | | `ayah`, `surah`, `juz`, `page` (default: `ayah`) |
| `verseNumber` | integer | For ayah | Verse number |
| `mushaf` | integer | ✓ | Mushaf ID (1-19) |

### Response (200)

```json
{
  "success": true,
  "data": {
    "id": "cmkg2wdxr00052o5rccy30b9g",
    "createdAt": "2023-01-21T07:28:13.023Z",
    "type": "ayah",
    "key": 1,
    "verseNumber": 5,
    "group": "string"
  }
}
```

---

## Get All Bookmarks

Retrieve user's bookmarks with pagination.

```
GET /bookmarks
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | Filter: `ayah`, `surah`, `juz`, `page` |
| `mushafId` | integer | Filter by Mushaf ID |
| `first` | integer | Items to fetch (1-20) |
| `after` | string | Cursor for pagination |
| `last` | integer | Items from end (1-20) |
| `before` | string | Cursor for reverse pagination |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "cmkg2wdxr00052o5rccy30b9g",
      "createdAt": "2023-01-21T07:28:13.023Z",
      "type": "ayah",
      "key": 1,
      "verseNumber": 5
    }
  ],
  "pagination": {
    "startCursor": "cmkg2wdjp00022o5r9b7x3au2",
    "endCursor": "cmkg2wdjp00032o5rf27ce2l2",
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

---

## Check Bookmark Exists

Check if a specific bookmark exists.

```
GET /bookmarks/exists
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key` | integer | ✓ | Surah/Juz/page number |
| `type` | string | | Bookmark type |
| `verseNumber` | integer | For ayah | Verse number |
| `mushafId` | integer | ✓ | Mushaf ID |

### Response (200)

```json
{
  "success": true,
  "data": {
    "exists": true
  }
}
```

---

## Delete Bookmark

Remove a bookmark by details.

```
DELETE /bookmarks
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key` | integer | ✓ | Surah/Juz/page number |
| `type` | string | | Bookmark type |
| `verseNumber` | integer | For ayah | Verse number |
| `mushafId` | integer | ✓ | Mushaf ID |

### Response (200)

```json
{
  "success": true,
  "data": {
    "message": "bookmark deleted"
  }
}
```

---

## Get Bookmark Collections

Get all collections a bookmark belongs to.

```
GET /bookmarks/collections
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key` | float | ✓ | Surah/Juz/page number |
| `type` | string | | `page`, `juz`, `surah`, `ayah` |
| `mushafId` | integer | ✓ | Mushaf ID |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "cmkg2we2000072o5r6vqjgv4a",
      "updatedAt": "2023-01-21T07:28:13.023Z",
      "name": "Woman in Quran"
    }
  ]
}
```

---

## Examples

### Add Ayat al-Kursi Bookmark

```bash
curl -X POST https://apis-prelive.quran.foundation/api/v1/bookmarks \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"key": 2, "type": "ayah", "verseNumber": 255, "mushaf": 1}'
```

### Get All Ayah Bookmarks

```bash
curl "https://apis-prelive.quran.foundation/api/v1/bookmarks?type=ayah&first=20" \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID"
```

### Delete a Bookmark

```bash
curl -X DELETE "https://apis-prelive.quran.foundation/api/v1/bookmarks?key=2&verseNumber=255&mushafId=1" \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID"
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
