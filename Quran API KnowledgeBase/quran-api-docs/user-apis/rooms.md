# Rooms/Groups API

> Community groups for sharing reflections  
> **Base Path:** `/api/v1/rooms`

---

## Overview

Rooms (also called Groups) are community spaces where users can share posts, reflections, and discussions about the Quran.

---

## Endpoints (24 total)

### Room Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rooms` | Create a room |
| GET | `/rooms` | List rooms |
| GET | `/rooms/{roomId}` | Get room details |
| PUT | `/rooms/{roomId}` | Update room |
| DELETE | `/rooms/{roomId}` | Delete room |

### Membership
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rooms/{roomId}/join` | Join room |
| POST | `/rooms/{roomId}/leave` | Leave room |
| GET | `/rooms/{roomId}/members` | List members |
| POST | `/rooms/{roomId}/invite` | Invite user |
| DELETE | `/rooms/{roomId}/members/{userId}` | Remove member |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rooms/admins` | Update admin access |
| GET | `/rooms/{roomId}/admins` | List admins |

---

## Create Room

Create a new community group.

```
POST /rooms
Content-Type: application/json
```

### Request Body

```json
{
  "name": "Tafsir Study Circle",
  "description": "Weekly study of Ibn Kathir's tafsir",
  "url": "tafsir-study",
  "public": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Room name (max 50 chars) |
| `description` | string | | Description (max 200 chars) |
| `url` | string | ✓ | URL slug (max 50 chars) |
| `public` | boolean | | Public visibility |

### Response (201)

```json
{
  "success": true,
  "data": {
    "id": 123,
    "name": "Tafsir Study Circle",
    "url": "tafsir-study",
    "public": true,
    "ownerId": "user123",
    "memberCount": 1
  }
}
```

---

## Update Admin Access

Grant or revoke admin privileges.

```
POST /rooms/admins
Content-Type: application/json
```

### Request Body

```json
{
  "roomId": 123,
  "userId": "user456",
  "admin": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `roomId` | integer | ✓ | Room ID |
| `userId` | string | ✓ | User ID |
| `admin` | boolean | ✓ | Grant (true) or revoke (false) |

### Response (200)

```json
{
  "success": true
}
```

---

## Join Room

Join a public room or accept invitation.

```
POST /rooms/{roomId}/join
```

---

## Leave Room

Leave a room.

```
POST /rooms/{roomId}/leave
```

---

## Room Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique room ID |
| `name` | string | Room name |
| `description` | string | Room description |
| `url` | string | URL slug |
| `public` | boolean | Public visibility |
| `ownerId` | string | Owner user ID |
| `memberCount` | integer | Number of members |
| `createdAt` | datetime | Creation date |

---

## Examples

### Create a Private Room

```bash
curl -X POST https://apis-prelive.quran.foundation/api/v1/rooms \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Family Quran Study",
    "description": "Private family study group",
    "url": "family-study",
    "public": false
  }'
```

### Grant Admin Access

```bash
curl -X POST https://apis-prelive.quran.foundation/api/v1/rooms/admins \
  -H "x-auth-token: TOKEN" \
  -H "x-client-id: CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{"roomId": 123, "userId": "user456", "admin": true}'
```

---

*[Back to User APIs](README.md) | [Back to Main Index](../README.md)*
