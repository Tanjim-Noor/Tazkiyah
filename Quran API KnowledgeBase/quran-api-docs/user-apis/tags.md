# Tags API

> Content categorization  
> **Base Path:** `/api/v1/tags`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tags` | Search/list tags |

---

## Search Tags

Find tags by query.

```
GET /tags
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search term |
| `limit` | integer | Max results |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "tag123",
      "name": "patience",
      "usageCount": 150
    },
    {
      "id": "tag456",
      "name": "gratitude",
      "usageCount": 89
    }
  ]
}
```

---

## Tag Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Tag ID |
| `name` | string | Tag name |
| `usageCount` | integer | Times used |

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
