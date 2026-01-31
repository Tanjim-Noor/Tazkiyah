# Collections API

> Organize bookmarks into named groups  
> **Base Path:** `/api/v1/collections`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/collections` | Create a collection |
| GET | `/collections` | Get all collections |
| GET | `/collections/items` | Get all collection items |
| GET | `/collections/{id}/items` | Get items in a collection |
| POST | `/collections/{id}/bookmarks` | Add bookmark to collection |
| DELETE | `/collections/{id}/bookmarks` | Remove bookmark from collection |
| PATCH | `/collections/{id}` | Update collection |
| DELETE | `/collections/{id}` | Delete collection |

---

## Create Collection

Create a new bookmark collection.

```
POST /collections
Content-Type: application/json
```

### Request Body

```json
{
  "name": "Favorite Ayat"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Collection name |

### Response (200)

```json
{
  "success": true,
  "data": {
    "id": "cmkg2we2000072o5r6vqjgv4a",
    "createdAt": "2023-01-21T07:28:13.023Z",
    "name": "Favorite Ayat"
  }
}
```

---

## Get All Collections

List all user collections.

```
GET /collections
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `first` | integer | Items to fetch (1-20) |
| `after` | string | Cursor for pagination |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "cmkg2we2000072o5r6vqjgv4a",
      "updatedAt": "2023-01-21T07:28:13.023Z",
      "name": "Favorite Ayat"
    }
  ],
  "pagination": {
    "startCursor": "...",
    "endCursor": "...",
    "hasNextPage": false,
    "hasPreviousPage": false
  }
}
```

---

## Get All Collection Items

Get bookmarks across all collections.

```
GET /collections/items
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sortBy` | string | `recentlyAdded` or `verseKey` |
| `type` | string | `page`, `juz`, `surah`, `ayah` |
| `first` | integer | Items to fetch (1-20) |
| `after` | string | Cursor for pagination |

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
      "verseNumber": 5,
      "group": "string"
    }
  ],
  "pagination": {...}
}
```

---

## Get Collection Items by ID

Get bookmarks in a specific collection.

```
GET /collections/{collectionId}/items
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collectionId` | string | ✓ | Collection ID |

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sortBy` | string | `recentlyAdded` or `verseKey` |
| `type` | string | Bookmark type filter |
| `first` | integer | Items to fetch |

---

## Add Bookmark to Collection

Add an existing or new bookmark to a collection.

```
POST /collections/{collectionId}/bookmarks
Content-Type: application/json
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collectionId` | string | ✓ | Collection ID |

### Request Body (Ayah)

```json
{
  "key": 2,
  "type": "ayah",
  "verseNumber": 255,
  "mushaf": 1
}
```

### Request Body (Surah/Juz/Page)

```json
{
  "key": 36,
  "type": "surah",
  "mushaf": 1
}
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "message": "collection bookmark added"
  }
}
```

---

## Delete Bookmark from Collection

Remove a bookmark from a collection.

```
DELETE /collections/{collectionId}/bookmarks
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key` | integer | ✓ | Surah/Juz/page number |
| `type` | string | | Bookmark type |
| `verseNumber` | integer | For ayah | Verse number |
| `mushafId` | integer | ✓ | Mushaf ID |

---

## Update Collection

Rename a collection.

```
PATCH /collections/{collectionId}
Content-Type: application/json
```

### Request Body

```json
{
  "name": "New Collection Name"
}
```

---

## Delete Collection

Remove a collection and all its bookmarks.

```
DELETE /collections/{collectionId}
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "message": "collection deleted"
  }
}
```

---

## Examples

### Create a Collection

```bash
curl -X POST https://apis-prelive.quran.foundation/api/v1/collections \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"name": "Daily Recitation"}'
```

### Add Ayat al-Kursi to Collection

```bash
curl -X POST https://apis-prelive.quran.foundation/api/v1/collections/COLLECTION_ID/bookmarks \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"key": 2, "type": "ayah", "verseNumber": 255, "mushaf": 1}'
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
