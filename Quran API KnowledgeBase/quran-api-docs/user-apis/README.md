# User-Related APIs (v1.0.0)

> Authenticated user-centric features  
> **Base URL:** `https://apis-prelive.quran.foundation`

---

## Overview

User-related APIs enable integration with Quran Foundation's personalized features including bookmarks, collections, notes, goals, streaks, reading sessions, and social features. These APIs require OAuth2 authentication.

---

## Authentication

All endpoints require:

```
x-auth-token: <JWT access token>
x-client-id: <Your client ID>
```

See [OAuth2 APIs](../oauth2-apis/README.md) for obtaining tokens.

---

## Pagination

User APIs use **cursor-based pagination**:

| Parameter | Description |
|-----------|-------------|
| `first` | Number of items (1-20), use with `after` |
| `after` | Cursor for next page |
| `last` | Number of items (1-20), use with `before` |
| `before` | Cursor for previous page |

**Rules:**
- Use `first` + `after` OR `last` + `before`
- Don't mix forward and backward pagination

**Response:**
```json
{
  "pagination": {
    "startCursor": "cmkg2wdjp00022o5r9b7x3au2",
    "endCursor": "cmkg2wdjp00032o5rf27ce2l2",
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

---

## API Sections

| Section | Endpoints | File |
|---------|-----------|------|
| Collections | 8 | [collections.md](collections.md) |
| Bookmarks | 6 | [bookmarks.md](bookmarks.md) |
| Notes | 10 | [notes.md](notes.md) |
| Preferences | 3 | [preferences.md](preferences.md) |
| Reading Sessions | 2 | [reading-sessions.md](reading-sessions.md) |
| Goals | 5 | [goals.md](goals.md) |
| Streaks | 2 | [streaks.md](streaks.md) |
| Activity Days | 3 | [activity-days.md](activity-days.md) |
| Users | 11 | [users.md](users.md) |
| Rooms/Groups | 24 | [rooms.md](rooms.md) |
| Posts | 16 | [posts.md](posts.md) |
| Comments | 4 | [comments.md](comments.md) |
| Tags | 1 | [tags.md](tags.md) |

---

## Quick Start

### 1. Get Access Token

```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Authorization: Basic $(echo -n 'client_id:secret' | base64)" \
  -d "grant_type=authorization_code&code=AUTH_CODE&redirect_uri=..."
```

### 2. Make Authenticated Request

```bash
curl https://apis-prelive.quran.foundation/api/v1/bookmarks \
  -H "x-auth-token: YOUR_ACCESS_TOKEN" \
  -H "x-client-id: YOUR_CLIENT_ID"
```

---

## Common Response Format

### Success

```json
{
  "success": true,
  "data": {...}
}
```

### Error

```json
{
  "success": false,
  "message": "Error description",
  "type": "error_type"
}
```

---

## Error Types

| Status | Type | Description |
|--------|------|-------------|
| 400 | `invalid_request` | Missing/invalid parameters |
| 401 | `unauthorized` | Authentication required |
| 403 | `forbidden` | Insufficient permissions |
| 404 | `not_found` | Resource not found |
| 422 | `unprocessable_entity` | Validation error |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_server_error` | Server error |

---

## Mushaf IDs Reference

Used in bookmark and collection endpoints:

| ID | Name |
|----|------|
| 1 | QCFV2 |
| 2 | QCFV1 |
| 3 | Indopak |
| 4 | UthmaniHafs |
| 5 | KFGQPCHAFS |
| 6 | Indopak15Lines |
| 7 | Indopak16Lines |
| 11 | Tajweed |
| 19 | QCFTajweedV4 |

---

*[Back to Main Index](../README.md)*
