# Notes API

> Personal annotations and reflections on verses  
> **Base Path:** `/api/v1/notes`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get all notes |
| POST | `/notes` | Create a note |
| GET | `/notes/{noteId}` | Get note by ID |
| PUT | `/notes/{noteId}` | Update note |
| DELETE | `/notes/{noteId}` | Delete note |
| GET | `/notes/by-range` | Get notes by verse range |
| POST | `/notes/{noteId}/entities` | Attach entity to note |
| DELETE | `/notes/{noteId}/entities` | Remove entity from note |
| POST | `/notes/{noteId}/ranges` | Add verse range |
| DELETE | `/notes/{noteId}/ranges` | Remove verse range |

---

## Get All Notes

Retrieve user's notes with pagination.

```
GET /notes
```

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cursor` | string | | Pagination cursor |
| `limit` | integer | 20 | Max notes (1-50) |
| `sortBy` | string | `newest` | `newest` or `oldest` |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "asdasdqwe1231",
      "createdAt": "2023-01-21T07:28:13.023Z",
      "updatedAt": "2023-01-22T07:28:13.023Z",
      "body": "This is a sample note body.",
      "source": "we23412312weq",
      "attachedEntities": [
        {
          "entityId": "entity123",
          "entityType": "reflection",
          "entityMetadata": {"key": "value"}
        }
      ],
      "ranges": ["2:255-2:257"]
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

## Create Note

Create a new note.

```
POST /notes
Content-Type: application/json
```

### Request Body

```json
{
  "body": "Personal reflection on Ayat al-Kursi...",
  "ranges": ["2:255-2:255"],
  "saveToQR": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | string | ✓ | Note content (6-10000 chars) |
| `ranges` | string[] | | Verse ranges (`chapter:verse-chapter:verse`) |
| `saveToQR` | boolean | | Save to QuranReflect (default: false) |

### Response (200)

```json
{
  "success": true,
  "data": {
    "id": "asdasdqwe1231",
    "createdAt": "2023-01-21T07:28:13.023Z",
    "updatedAt": "2023-01-21T07:28:13.023Z",
    "body": "Personal reflection on Ayat al-Kursi...",
    "ranges": ["2:255-2:255"]
  }
}
```

---

## Get Note by ID

Retrieve a specific note.

```
GET /notes/{noteId}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `noteId` | string | ✓ | Note ID |

---

## Update Note

Modify an existing note.

```
PUT /notes/{noteId}
Content-Type: application/json
```

### Request Body

```json
{
  "body": "Updated note content...",
  "saveToQR": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | string | ✓ | Updated content (6-10000 chars) |
| `saveToQR` | boolean | | Sync to QuranReflect |

---

## Delete Note

Remove a note.

```
DELETE /notes/{noteId}
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "message": "note deleted"
  }
}
```

---

## Get Notes by Verse Range

Find notes associated with specific verses.

```
GET /notes/by-range
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `range` | string | ✓ | Verse range (e.g., `2:255-2:260`) |

---

## Verse Range Format

Ranges use the format: `chapter:verse-chapter:verse`

Examples:
- Single verse: `2:255-2:255`
- Verse span: `2:255-2:257`
- Cross-chapter: `2:285-3:5`

Pattern: `^(\d+):(\d+)-(\d+):(\d+)$`

---

## Note Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `createdAt` | datetime | Creation timestamp |
| `updatedAt` | datetime | Last update timestamp |
| `body` | string | Note content (6-10000 chars) |
| `source` | string | Optional source reference |
| `attachedEntities` | array | Linked entities (reflections) |
| `ranges` | string[] | Associated verse ranges |

---

## Examples

### Create Note on Ayat al-Kursi

```bash
curl -X POST https://apis-prelive.quran.foundation/api/v1/notes \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "body": "The Throne Verse - a powerful reminder of Allah'\''s sovereignty...",
    "ranges": ["2:255-2:255"]
  }'
```

### Get All Notes (Newest First)

```bash
curl "https://apis-prelive.quran.foundation/api/v1/notes?sortBy=newest&limit=10" \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID"
```

### Update a Note

```bash
curl -X PUT https://apis-prelive.quran.foundation/api/v1/notes/NOTE_ID \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"body": "Updated reflection with deeper insights..."}'
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
