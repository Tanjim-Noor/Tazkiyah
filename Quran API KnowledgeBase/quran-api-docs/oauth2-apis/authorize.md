# Authorization Endpoint

> Initiate OAuth2 authorization flow  
> **Endpoint:** `GET /oauth2/authorize`

---

## Request

```
GET /oauth2/authorize
```

### Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `response_type` | ✓ | `code`, `token`, or `id_token` |
| `client_id` | ✓ | Your client ID |
| `redirect_uri` | ✓ | Callback URL (must be registered) |
| `scope` | | Space-separated scopes |
| `state` | Recommended | Random string for CSRF protection |
| `nonce` | For `id_token` | Random string for replay protection |
| `code_challenge` | For PKCE | S256 hash of code verifier |
| `code_challenge_method` | For PKCE | `S256` |

---

## Response Types

### Authorization Code (`response_type=code`)

User is redirected to your `redirect_uri` with:

```
https://yourapp.com/callback?code=AUTH_CODE&state=YOUR_STATE
```

### Implicit Token (`response_type=token`)

Token returned in URL fragment:

```
https://yourapp.com/callback#access_token=TOKEN&token_type=bearer&expires_in=3600&state=YOUR_STATE
```

### ID Token (`response_type=id_token`)

OpenID Connect implicit flow:

```
https://yourapp.com/callback#id_token=JWT&state=YOUR_STATE
```

---

## PKCE Flow (Recommended for Public Clients)

### 1. Generate Code Verifier

Random 43-128 character string:
```
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

### 2. Create Code Challenge

SHA256 hash, base64url encoded:
```
code_challenge = base64url(sha256(code_verifier))
```

### 3. Authorization Request

```
GET /oauth2/authorize
  ?response_type=code
  &client_id=YOUR_CLIENT_ID
  &redirect_uri=https://yourapp.com/callback
  &scope=openid user
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
  &state=abc123
```

### 4. Token Exchange with Verifier

```bash
curl -X POST /oauth2/token \
  -d "grant_type=authorization_code" \
  -d "code=AUTH_CODE" \
  -d "redirect_uri=https://yourapp.com/callback" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
```

---

## Error Responses

Errors are returned to `redirect_uri`:

```
https://yourapp.com/callback?error=ERROR_CODE&error_description=DESCRIPTION&state=YOUR_STATE
```

### Error Codes

| Error | Description |
|-------|-------------|
| `invalid_request` | Missing or invalid parameter |
| `unauthorized_client` | Client not authorized |
| `access_denied` | User denied consent |
| `unsupported_response_type` | Response type not supported |
| `invalid_scope` | Scope invalid or unknown |
| `server_error` | Server error |
| `temporarily_unavailable` | Service unavailable |

---

## Example Flow

### Step 1: Build Authorization URL

```javascript
const authUrl = new URL('https://apis-prelive.quran.foundation/oauth2/authorize');
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('client_id', 'YOUR_CLIENT_ID');
authUrl.searchParams.set('redirect_uri', 'https://yourapp.com/callback');
authUrl.searchParams.set('scope', 'openid user collection bookmark');
authUrl.searchParams.set('state', crypto.randomUUID());

// Redirect user
window.location.href = authUrl.toString();
```

### Step 2: Handle Callback

```javascript
// At https://yourapp.com/callback?code=AUTH_CODE&state=STATE
const code = new URLSearchParams(window.location.search).get('code');
const state = new URLSearchParams(window.location.search).get('state');

// Verify state matches, then exchange code for tokens
```

---

*[Back to OAuth2 APIs](README.md) | [Back to Main Index](../README.md)*
