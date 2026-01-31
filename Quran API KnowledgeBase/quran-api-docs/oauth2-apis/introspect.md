# Token Introspection Endpoint

> Validate and inspect access tokens  
> **Endpoint:** `POST /oauth2/introspect`

---

## Request

```
POST /oauth2/introspect
Content-Type: application/x-www-form-urlencoded
Authorization: Basic <base64(client_id:client_secret)>
```

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | ✓ | `Basic <base64(client_id:client_secret)>` |
| `Content-Type` | ✓ | `application/x-www-form-urlencoded` |

### Body Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `token` | ✓ | The token to introspect |
| `token_type_hint` | | `access_token` or `refresh_token` |

---

## Response (200 OK)

### Active Token

```json
{
  "active": true,
  "scope": "openid user collection bookmark",
  "client_id": "your_client_id",
  "username": "johndoe",
  "token_type": "Bearer",
  "exp": 1670003600,
  "iat": 1670000000,
  "nbf": 1670000000,
  "sub": "user123",
  "aud": "your_client_id",
  "iss": "https://auth.quran.foundation"
}
```

### Inactive/Invalid Token

```json
{
  "active": false
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `active` | boolean | Whether token is valid |
| `scope` | string | Token scopes |
| `client_id` | string | Client that requested token |
| `username` | string | Resource owner username |
| `token_type` | string | Token type (`Bearer`) |
| `exp` | integer | Expiration timestamp |
| `iat` | integer | Issued at timestamp |
| `nbf` | integer | Not before timestamp |
| `sub` | string | Subject (user ID) |
| `aud` | string | Audience |
| `iss` | string | Issuer |

---

## Error Responses

### 401 Unauthorized

```json
{
  "error": "invalid_client",
  "error_description": "Client authentication failed"
}
```

---

## Example

```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/introspect \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic $(echo -n 'client_id:client_secret' | base64)" \
  -d "token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Use Cases

1. **Token Validation**: Verify tokens received from clients
2. **Scope Checking**: Confirm token has required permissions
3. **User Identification**: Get user info from token
4. **Debugging**: Inspect token contents

---

*[Back to OAuth2 APIs](README.md) | [Back to Main Index](../README.md)*
