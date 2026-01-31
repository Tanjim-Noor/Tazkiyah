# Quran Foundation API Documentation

> Complete API reference for the Quran Foundation platform  
> **Base URL:** `https://apis-prelive.quran.foundation`  
> **Documentation Source:** [api-docs.quran.foundation](https://api-docs.quran.foundation)

---

## Table of Contents

### 1. [Content APIs (v4)](content-apis/README.md)
Non-user-specific resources for Quran data access.

| Section | Description | Endpoints |
|---------|-------------|-----------|
| [Audio](content-apis/audio.md) | Recitations, chapter audio, verse audio | 5+ |
| [Chapters](content-apis/chapters.md) | Surah metadata and info | 3 |
| [Verses](content-apis/verses.md) | Ayah retrieval by various methods | 8+ |
| [Juz](content-apis/juz.md) | 30-part division endpoints | 2 |
| [Hizb](content-apis/hizb.md) | 60-part Hizb division | 2 |
| [Rub El Hizb](content-apis/rub-el-hizb.md) | 240 quarter-Hizb segments | 2 |
| [Ruku](content-apis/ruku.md) | Thematic paragraph groupings | 2 |
| [Manzil](content-apis/manzil.md) | 7-day reading division | 2 |
| [Translations](content-apis/translations.md) | Translation resources | 5+ |
| [Tafsirs](content-apis/tafsirs.md) | Exegesis/commentary | 3+ |
| [Resources](content-apis/resources.md) | Languages, recitations, scripts | 5 |
| [Quran](content-apis/quran.md) | Text retrieval endpoints | 3+ |

### 2. [Search APIs (v1.0)](search-apis/README.md)
Full-text search across Quran content.

| Endpoint | Description |
|----------|-------------|
| [Search Content](search-apis/search.md) | Search verses, chapters, juz, pages |

### 3. [User APIs (v1.0.0)](user-apis/README.md)
Authenticated user-centric features (requires OAuth2).

| Section | Description | Endpoints |
|---------|-------------|-----------|
| [Collections](user-apis/collections.md) | Organize bookmarks into groups | 8 |
| [Bookmarks](user-apis/bookmarks.md) | Save ayah/page/juz references | 6 |
| [Notes](user-apis/notes.md) | Personal annotations | 10 |
| [Goals](user-apis/goals.md) | Reading targets and plans | 5 |
| [Streaks](user-apis/streaks.md) | Consistency tracking | 2 |
| [Reading Sessions](user-apis/reading-sessions.md) | Progress tracking | 2 |
| [Preferences](user-apis/preferences.md) | User settings | 3 |
| [Activity Days](user-apis/activity-days.md) | Daily engagement metrics | 3 |
| [Users](user-apis/users.md) | Profile management | 11 |
| [Rooms/Groups](user-apis/rooms.md) | Community groups | 24 |
| [Posts](user-apis/posts.md) | Community reflections | 16 |
| [Comments](user-apis/comments.md) | Post interactions | 4 |
| [Tags](user-apis/tags.md) | Content categorization | 1 |

### 4. [OAuth2 APIs (v1.0.0)](oauth2-apis/README.md)
Authentication and authorization flows.

| Endpoint | Description |
|----------|-------------|
| [Token Exchange](oauth2-apis/token.md) | Obtain/refresh access tokens |
| [Authorize](oauth2-apis/authorize.md) | Authorization code flow |
| [Userinfo](oauth2-apis/userinfo.md) | OpenID Connect user claims |
| [Introspect](oauth2-apis/introspect.md) | Token validation |

---

## Authentication

### OAuth2 Scopes
| Scope | Description |
|-------|-------------|
| `collection` | Access user collections |
| `bookmark` | Access user bookmarks |
| `reading_session` | Access reading sessions |
| `preference` | Access user preferences |
| `user` | Access user profile |
| `search` | Search API access |
| `openid` | OpenID Connect identity |
| `offline_access` | Refresh token issuance |

### Authentication Headers
```
x-auth-token: <JWT access token>
x-client-id: <Your client ID>
```

### Token Request Example
```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic <base64(client_id:client_secret)>" \
  -d "grant_type=client_credentials&scope=search"
```

---

## Common Response Patterns

### Pagination (Content APIs)
```json
{
  "verses": [...],
  "pagination": {
    "per_page": 10,
    "current_page": 1,
    "next_page": 2,
    "total_pages": 5,
    "total_records": 50
  }
}
```

### Pagination (User APIs - Cursor-based)
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "startCursor": "cmkg2wdjp00022o5r9b7x3au2",
    "endCursor": "cmkg2wdjp00032o5rf27ce2l2",
    "hasNextPage": true,
    "hasPreviousPage": false
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description",
  "type": "error_type"
}
```

### Error Types
| Status | Type | Description |
|--------|------|-------------|
| 400 | `invalid_request` | Missing/invalid parameters |
| 401 | `unauthorized` | Authentication required |
| 403 | `forbidden` | Insufficient permissions |
| 404 | `not_found` | Resource doesn't exist |
| 422 | `unprocessable_entity` | Validation failed |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_server_error` | Server error |
| 502 | `bad_gateway` | Upstream error |
| 503 | `service_unavailable` | Maintenance/overload |
| 504 | `gateway_timeout` | Upstream timeout |

---

## Quick Start

### 1. Get All Chapters
```bash
curl https://apis-prelive.quran.foundation/content/api/v4/chapters
```

### 2. Get Verses with Translation
```bash
curl "https://apis-prelive.quran.foundation/content/api/v4/verses/by_chapter/1?translations=131&language=en"
```

### 3. Search Quran
```bash
curl -H "x-auth-token: <token>" -H "x-client-id: <id>" \
  "https://apis-prelive.quran.foundation/api/v1/search?q=mercy&size=10"
```

---

## Related Resources

- **JavaScript SDK:** [@quranjs/api](https://www.npmjs.com/package/@quranjs/api)
- **Official Documentation:** https://api-docs.quran.foundation
- **OAuth2 Tutorial:** https://api-docs.quran.foundation/docs/tutorials/oidc/getting-started-with-oauth2

---

*Generated from Quran Foundation API Documentation Portal*
