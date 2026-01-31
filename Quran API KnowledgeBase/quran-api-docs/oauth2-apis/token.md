# Token Exchange Endpoint

> Exchange credentials for access tokens  
> **Endpoint:** `POST /oauth2/token`

---

## Request

```
POST /oauth2/token
Content-Type: application/x-www-form-urlencoded
```

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | For `client_credentials` | `Basic <base64(client_id:client_secret)>` |
| `Content-Type` | ✓ | `application/x-www-form-urlencoded` |

### Body Parameters

#### Client Credentials Grant

| Parameter | Required | Description |
|-----------|----------|-------------|
| `grant_type` | ✓ | `client_credentials` |
| `scope` | | Space-separated scopes |

#### Authorization Code Grant

| Parameter | Required | Description |
|-----------|----------|-------------|
| `grant_type` | ✓ | `authorization_code` |
| `code` | ✓ | Authorization code from callback |
| `redirect_uri` | ✓ | Must match original request |
| `client_id` | ✓ | Your client ID |
| `code_verifier` | | PKCE code verifier |

#### Refresh Token Grant

| Parameter | Required | Description |
|-----------|----------|-------------|
| `grant_type` | ✓ | `refresh_token` |
| `refresh_token` | ✓ | The refresh token |
| `client_id` | ✓ | Your client ID |
| `scope` | | Scope for new token (subset only) |

---

## Response (200 OK)

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGgucXVyYW4uZm91bmRhdGlvbiIsInN1YiI6InVzZXIxMjMiLCJhdWQiOiJjbGllbnQxIiwiZXhwIjoxNjcwMDAwMDAwLCJpYXQiOjE2Njk5OTY0MDAsInNjb3BlIjoib3BlbmlkIHVzZXIgY29sbGVjdGlvbiJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "scope": "openid user collection bookmark"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT access token |
| `token_type` | string | Always `bearer` |
| `expires_in` | integer | Token lifetime in seconds |
| `refresh_token` | string | Token for refreshing (if `offline_access` scope) |
| `id_token` | string | OpenID Connect ID token (if `openid` scope) |
| `scope` | string | Granted scopes |

---

## Error Responses

### 400 Bad Request

```json
{
  "error": "invalid_grant",
  "error_description": "The authorization code has expired"
}
```

### 401 Unauthorized

```json
{
  "error": "invalid_client",
  "error_description": "Client authentication failed"
}
```

### Error Codes

| Error | Description |
|-------|-------------|
| `invalid_request` | Missing required parameter |
| `invalid_client` | Client authentication failed |
| `invalid_grant` | Invalid code or refresh token |
| `unauthorized_client` | Client not authorized for grant type |
| `unsupported_grant_type` | Grant type not supported |
| `invalid_scope` | Requested scope invalid |

---

## Examples

### Client Credentials

```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic $(echo -n 'my_client_id:my_client_secret' | base64)" \
  -d "grant_type=client_credentials&scope=search"
```

### Authorization Code Exchange

```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=SplxlOBeZQQYbYS6WxSbIA" \
  -d "redirect_uri=https://myapp.com/callback" \
  -d "client_id=my_client_id"
```

### Refresh Token

```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4" \
  -d "client_id=my_client_id"
```

---

*[Back to OAuth2 APIs](README.md) | [Back to Main Index](../README.md)*
