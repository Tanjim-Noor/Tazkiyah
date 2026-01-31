# Posts API

> Community reflections and sharing  
> **Base Path:** `/api/v1/posts`

---

## Overview

Posts are user-generated reflections on Quran verses, shared publicly or within rooms.

---

## Endpoints (16 total)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts/feed` | Get personalized feed |
| GET | `/posts` | List posts |
| POST | `/posts` | Create post |
| GET | `/posts/{postId}` | Get post details |
| PUT | `/posts/{postId}` | Update post |
| DELETE | `/posts/{postId}` | Delete post |
| POST | `/posts/{postId}/like` | Like/unlike post |
| GET | `/posts/{postId}/likes` | Get post likes |
| POST | `/posts/{postId}/save` | Save post |
| GET | `/posts/saved` | Get saved posts |
| POST | `/posts/{postId}/report` | Report post |
| GET | `/posts/by-verse/{verseKey}` | Posts for verse |

---

## Get Feed

Retrieve personalized post feed.

```
GET /posts/feed
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | string | `FOLLOWING`, `GLOBAL`, `ROOM` |
| `roomId` | integer | For room-specific feed |
| `limit` | integer | Posts per page |
| `cursor` | string | Pagination cursor |

### Response (200)

```json
{
  "success": true,
  "data": [
    {
      "id": "post123",
      "body": "Beautiful reflection on patience...",
      "verseRanges": ["2:153-2:153"],
      "author": {
        "id": "user456",
        "username": "scholar",
        "avatarUrls": {...}
      },
      "likesCount": 42,
      "commentsCount": 5,
      "liked": false,
      "saved": true,
      "createdAt": "2023-01-21T07:28:13.023Z"
    }
  ],
  "pagination": {...}
}
```

---

## Create Post

Share a reflection.

```
POST /posts
Content-Type: application/json
```

### Request Body

```json
{
  "body": "My reflection on Ayat al-Kursi...",
  "verseRanges": ["2:255-2:255"],
  "roomId": null,
  "language": "en"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | string | ✓ | Post content |
| `verseRanges` | string[] | | Associated verses |
| `roomId` | integer | | Post to specific room |
| `language` | string | | Content language |

---

## Like/Unlike Post

Toggle like on a post.

```
POST /posts/{postId}/like
```

### Response (200)

```json
{
  "liked": true,
  "likesCount": 43
}
```

---

## Get Posts by Verse

Find posts about a specific verse.

```
GET /posts/by-verse/{verseKey}
```

### Path Parameters

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| `verseKey` | string | `2:255` | Verse identifier |

---

## Post Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Post ID |
| `body` | string | Post content |
| `verseRanges` | string[] | Associated verses |
| `author` | object | Author details |
| `roomId` | integer | Room (if posted to room) |
| `likesCount` | integer | Number of likes |
| `commentsCount` | integer | Number of comments |
| `liked` | boolean | Current user liked |
| `saved` | boolean | Current user saved |
| `createdAt` | datetime | Creation timestamp |

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
