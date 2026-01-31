# Userinfo Endpoint

> Get OpenID Connect user claims  
> **Endpoint:** `GET /userinfo`

---

## Request

```
GET /userinfo
Authorization: Bearer <access_token>
```

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | ✓ | `Bearer <access_token>` |

---

## Response (200 OK)

```json
{
  "sub": "user123",
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "preferred_username": "johndoe",
  "email": "john@example.com",
  "email_verified": true,
  "picture": "https://example.com/avatar.jpg",
  "updated_at": 1670000000
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `sub` | string | Subject identifier (user ID) |
| `name` | string | Full name |
| `given_name` | string | First name |
| `family_name` | string | Last name |
| `preferred_username` | string | Username |
| `email` | string | Email address |
| `email_verified` | boolean | Email verification status |
| `picture` | string | Profile picture URL |
| `updated_at` | integer | Last update timestamp |

---

## Required Scopes

| Scope | Claims Returned |
|-------|-----------------|
| `openid` | `sub` |
| `profile` | `name`, `given_name`, `family_name`, `preferred_username`, `picture`, `updated_at` |
| `email` | `email`, `email_verified` |

---

## Error Responses

### 401 Unauthorized

```json
{
  "error": "invalid_token",
  "error_description": "The access token is expired or invalid"
}
```

### 403 Forbidden

```json
{
  "error": "insufficient_scope",
  "error_description": "The access token does not have the required scope"
}
```

---

## Example

```bash
curl https://apis-prelive.quran.foundation/userinfo \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

*[Back to OAuth2 APIs](README.md) | [Back to Main Index](../README.md)*
