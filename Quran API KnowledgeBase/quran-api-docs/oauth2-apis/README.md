# OAuth2 APIs (v1.0.0)

> Authentication and authorization for Quran Foundation services  
> **Base URL:** `https://apis-prelive.quran.foundation`

---

## Overview

Quran Foundation uses OAuth2 for authentication. User-related APIs require an access token obtained through these OAuth2 endpoints.

---

## Authentication Methods

### Bearer Token (Recommended)
```
Authorization: Bearer <access_token>
```

### API Key Headers
```
x-auth-token: <JWT access token>
x-client-id: <Your client ID>
```

### Basic Auth (Token Endpoint)
```
Authorization: Basic <base64(client_id:client_secret)>
```

---

## OAuth2 Scopes

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

---

## Endpoints

| Endpoint | Description | File |
|----------|-------------|------|
| `POST /oauth2/token` | Token exchange | [token.md](token.md) |
| `GET /oauth2/authorize` | Authorization flow | [authorize.md](authorize.md) |
| `GET /userinfo` | User claims | [userinfo.md](userinfo.md) |
| `POST /oauth2/introspect` | Token validation | [introspect.md](introspect.md) |

---

## Grant Types

| Grant Type | Use Case |
|------------|----------|
| `client_credentials` | Server-to-server (no user) |
| `authorization_code` | User authorization flow |
| `refresh_token` | Token refresh |

---

## Token Response

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "abc123...",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "scope": "openid user collection bookmark"
}
```

---

## Quick Start

### 1. Client Credentials Flow (Server-to-Server)

```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Authorization: Basic $(echo -n 'client_id:client_secret' | base64)" \
  -d "grant_type=client_credentials&scope=search"
```

### 2. Authorization Code Flow

1. Redirect user to authorization endpoint:
```
GET /oauth2/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT&scope=openid%20user
```

2. Exchange code for tokens:
```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=AUTH_CODE&redirect_uri=YOUR_REDIRECT&client_id=YOUR_CLIENT_ID"
```

### 3. Refresh Token

```bash
curl -X POST https://apis-prelive.quran.foundation/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&refresh_token=YOUR_REFRESH_TOKEN&client_id=YOUR_CLIENT_ID"
```

---

## Getting OAuth2 Credentials

Follow the tutorial at:
https://api-docs.quran.foundation/docs/tutorials/oidc/getting-started-with-oauth2

---

*[Back to Main Index](../README.md)*
