# Comments API

> Post interactions and discussions  
> **Base Path:** `/api/v1/comments`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts/{postId}/comments` | Get post comments |
| POST | `/posts/{postId}/comments` | Add comment |
| PUT | `/comments/{commentId}` | Update comment |
| DELETE | `/comments/{commentId}` | Delete comment |

---

## Get Comments

List comments on a post.

```
GET /posts/{postId}/comments
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Comments per page |
| `cursor` | string | Pagination cursor |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "comment123",
      "body": "Jazakallah for sharing!",
      "author": {
        "id": "user789",
        "username": "reader",
        "avatarUrls": {...}
      },
      "createdAt": "2023-01-21T08:00:00.000Z"
    }
  ],
  "pagination": {...}
}
```

---

## Add Comment

Comment on a post.

```
POST /posts/{postId}/comments
Content-Type: application/json
```

### Request Body

```json
{
  "body": "Beautiful insight, thank you for sharing!"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | string | ✓ | Comment text |

---

## Update Comment

Edit a comment.

```
PUT /comments/{commentId}
Content-Type: application/json
```

### Request Body

```json
{
  "body": "Updated comment text"
}
```

---

## Delete Comment

Remove a comment.

```
DELETE /comments/{commentId}
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
