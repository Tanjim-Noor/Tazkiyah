# Users API

> User profile and social features  
> **Base Path:** `/api/v1/users`

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update profile |
| GET | `/users/search` | Search users |
| GET | `/users/{userId}` | Get user by ID |
| POST | `/users/{userId}/follow` | Follow/unfollow user |
| GET | `/users/{userId}/followers` | Get followers |
| GET | `/users/{userId}/following` | Get following |
| DELETE | `/users/me` | Delete account |

---

## Get Current User

Retrieve authenticated user's profile.

```
GET /users/me
```

### Response (200)

```json
{
  "success": true,
  "data": {
    "id": "user123",
    "username": "johndoe",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "bio": "Seeking knowledge...",
    "avatarUrls": {
      "small": "https://...",
      "medium": "https://...",
      "large": "https://..."
    },
    "followersCount": 150,
    "postsCount": 42,
    "verified": false,
    "createdAt": "2023-01-01T00:00:00.000Z"
  }
}
```

---

## Update Profile

Modify user profile.

```
PUT /users/me
Content-Type: application/json
```

### Request Body

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "bio": "Updated bio...",
  "username": "johndoe"
}
```

---

## Search Users

Find users by name or username.

```
GET /users/search
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search term |
| `limit` | integer | Results per page (default: 10) |
| `page` | integer | Page number |
| `all` | boolean | Search all users |
| `roomId` | integer | Scope to room |

### Response (200)

```json
{
  "total": 10,
  "currentPage": 1,
  "limit": 10,
  "pages": 1,
  "data": [
    {
      "id": "user456",
      "username": "scholar",
      "firstName": "Islamic",
      "lastName": "Scholar",
      "avatarUrls": {...},
      "verified": true,
      "followed": false
    }
  ]
}
```

---

## Follow/Unfollow User

Toggle follow status.

```
POST /users/{followeeId}/follow
Content-Type: application/json
```

### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `followeeId` | string | User ID to follow |

### Request Body (Optional)

```json
{
  "action": "follow"
}
```

| Field | Value | Description |
|-------|-------|-------------|
| `action` | `follow` | Force follow |
| `action` | `unfollow` | Force unfollow |

### Response (200)

```json
{
  "followed": true
}
```

---

## Get Followers

List user's followers.

```
GET /users/{userId}/followers
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Results per page |
| `page` | integer | Page number |

---

## Get Following

List users being followed.

```
GET /users/{userId}/following
```

---

## Delete Account

Permanently delete user account.

```
DELETE /users/me
```

⚠️ **Warning**: This action is irreversible.

---

## User Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique user ID |
| `username` | string | Display username |
| `firstName` | string | First name |
| `lastName` | string | Last name |
| `email` | string | Email (own profile only) |
| `bio` | string | Profile bio |
| `avatarUrls` | object | Avatar image URLs |
| `followersCount` | integer | Number of followers |
| `postsCount` | integer | Number of posts |
| `verified` | boolean | Verified account |
| `banned` | boolean | Account status |
| `createdAt` | datetime | Registration date |

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
