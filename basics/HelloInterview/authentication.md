# Authentication

## Overview

Authentication is the process of verifying the identity of a user, system, or entity attempting to access a resource.

---

## Core Concepts

### Authentication vs Authorization
- **Authentication (AuthN):** Who are you? (verifying identity)
- **Authorization (AuthZ):** What can you do? (verifying permissions)

---

## Common Authentication Methods

### 1. Password-Based Authentication
- User provides username + password
- Server hashes and compares against stored hash
- **Weaknesses:** phishing, brute force, credential stuffing

### 2. Token-Based Authentication (JWT)
- After login, server issues a signed token (JWT)
- Client sends token in `Authorization: Bearer <token>` header on subsequent requests
- **Stateless** — server does not store session
- **Structure:** `header.payload.signature`

### 3. Session-Based Authentication
- Server creates a session after login and stores it (in-memory, Redis, DB)
- Client receives a session cookie
- **Stateful** — server must look up the session on each request

### 4. OAuth 2.0
- Delegated authorization framework
- Allows a user to grant a third-party app access to their resources without sharing credentials
- **Roles:** Resource Owner, Client, Authorization Server, Resource Server
- **Grant Types:** Authorization Code, Client Credentials, Implicit (deprecated), Device Code

### 5. OpenID Connect (OIDC)
- Identity layer built on top of OAuth 2.0
- Provides an **ID Token** (JWT) with user identity information
- Used for Single Sign-On (SSO)

### 6. Multi-Factor Authentication (MFA)
- Combines two or more factors:
  - **Something you know:** password, PIN
  - **Something you have:** OTP, hardware key (TOTP/HOTP)
  - **Something you are:** biometrics

### 7. API Key Authentication
- Long-lived secret token passed in headers or query params
- Typically used for service-to-service communication
- No user identity context

### 8. mTLS (Mutual TLS)
- Both client and server present certificates
- Common in microservice-to-microservice communication

---

## Token Storage

| Location | XSS Risk | CSRF Risk | Notes |
|----------|----------|-----------|-------|
| `localStorage` | High | None | Accessible to JS |
| `sessionStorage` | High | None | Cleared on tab close |
| `HttpOnly Cookie` | None | High | Use CSRF tokens to mitigate |
| Memory (JS var) | Low | None | Lost on refresh |

**Best practice:** Store tokens in `HttpOnly`, `Secure`, `SameSite=Strict` cookies.

---

## JWT Deep Dive

```
Header:  { "alg": "HS256", "typ": "JWT" }
Payload: { "sub": "user123", "exp": 1700000000, "roles": ["admin"] }
Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)
```

### Key Considerations
- **Expiry (`exp`):** Keep access tokens short-lived (5–15 min)
- **Refresh tokens:** Long-lived, stored securely, used to obtain new access tokens
- **Revocation:** JWTs are stateless — use a blocklist or short expiry for revocation
- **Algorithm:** Prefer `RS256` (asymmetric) over `HS256` (shared secret) for distributed systems
  - Auth Server holds the **private key** (signs tokens); all other services hold only the **public key** (verify tokens)
  - Public key can be published openly (e.g. `/.well-known/jwks.json`); private key never leaves the Auth Server
  - Any service can verify a token locally — no callback to the Auth Server needed

### Concrete Example

**Scenario:** User logs into a web app. Server issues a short-lived access token and a long-lived refresh token.

**Token components:**
```
Header (base64url):  eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9
  → { "alg": "RS256", "typ": "JWT" }

Payload (base64url): eyJzdWIiOiJ1c2VyXzQ0MiIsImVtYWlsIjoiYWxpY2VAZXhhbXBsZS5jb20iLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTcwMDAwMDAwMCwiZXhwIjoxNzAwMDAwOTAwfQ
  → {
       "sub": "user_442",
       "email": "alice@example.com",
       "roles": ["user"],
       "iat": 1700000000,   // issued at
       "exp": 1700000900    // expires in 15 min
     }

Signature: <RS256 signature using Auth Server's private key>
```

**Full token sent by client:**
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzQ0Mi4....<signature>
```

**Server-side validation steps:**
1. Split on `.` → header, payload, signature
2. Verify `alg` is `RS256` (reject `none` or unexpected algorithms)
3. Verify signature using Auth Server's **public key** (no shared secret needed)
4. Check `exp` — reject if token is expired
5. Optionally check `iss` (issuer) and `aud` (audience) claims
6. Extract `sub` / `roles` for authorization decisions

### Flow

```mermaid
sequenceDiagram
    participant Client
    participant AuthServer as Auth Server
    participant API as Resource Server

    %% --- Login ---
    Client->>AuthServer: POST /login {email, password}
    AuthServer->>AuthServer: verify credentials, sign JWT (RS256)
    AuthServer-->>Client: 200 { access_token (15 min), refresh_token (7 days) }

    %% --- Authenticated request ---
    Client->>API: GET /api/orders\nAuthorization: Bearer <access_token>
    API->>API: verify signature with public key\ncheck exp, iss, aud
    API-->>Client: 200 { orders: [...] }

    %% --- Token refresh ---
    Note over Client,API: 15 minutes later — access token expires
    Client->>AuthServer: POST /token/refresh { refresh_token }
    AuthServer->>AuthServer: validate refresh token (DB lookup / blocklist check)
    AuthServer-->>Client: 200 { new_access_token (15 min) }

    %% --- Logout / revocation ---
    Note over Client,AuthServer: User logs out
    Client->>AuthServer: POST /logout { refresh_token }
    AuthServer->>AuthServer: add refresh_token to blocklist
    AuthServer-->>Client: 204 No Content
```

---

## Session-Based Authentication Deep Dive

```
Login:    Client sends credentials → Server creates session → stores in session store
Request:  Client sends session cookie → Server looks up session → returns data
Logout:   Server deletes session from store → cookie is invalidated
```

### Key Considerations
- **Stateful:** Session data lives on the server (in-memory, Redis, DB) — every request requires a store lookup
- **Revocation:** Instant — just delete the session from the store
- **Scaling:** Sessions must be shared across server instances; use a central store (Redis) instead of sticky sessions (sticky sessions tie a user to one instance — if it goes down, the session is lost)
- **Cookie flags:** Always set `HttpOnly`, `Secure`, `SameSite=Strict` to reduce XSS and CSRF exposure
- **Session ID:** Must be a long, random, unpredictable string (e.g. 128-bit random) — never derived from user data
- **Fixation:** Regenerate the session ID after login to prevent session fixation attacks
- **Timeout:** Enforce both idle timeout (e.g. 30 min inactivity) and absolute timeout (e.g. 24 hr max)

### Concrete Example

**Scenario:** User logs into a web app. Server creates a session and stores it in Redis.

**What the server stores in Redis:**
```
Key:   sess:a3f8c2d1e9b74f6a8c2d1e9b74f6a8c2
Value: {
         "userId": "user_442",
         "email": "alice@example.com",
         "roles": ["user"],
         "createdAt": 1700000000,
         "lastSeenAt": 1700000000
       }
TTL:   1800 (30 min idle timeout)
```

**Cookie sent to client:**
```
Set-Cookie: sessionId=a3f8c2d1e9b74f6a8c2d1e9b74f6a8c2; HttpOnly; Secure; SameSite=Strict; Path=/
```

**Server-side validation steps on each request:**
1. Read `sessionId` from cookie
2. Look up key `sess:<sessionId>` in Redis
3. If missing or expired → 401, redirect to login
4. If found → load user data, reset TTL (sliding expiry)
5. Attach user context to request and proceed

### Flow

```mermaid
sequenceDiagram
    participant Client
    participant Server
    participant Redis as Session Store (Redis)

    %% --- Login ---
    Client->>Server: POST /login
    Server->>Server: verify credentials
    Server->>Redis: SET sess-id to userId+roles, TTL 1800
    Server-->>Client: 200 + Set-Cookie sessionId=id HttpOnly Secure

    %% --- Authenticated request ---
    Client->>Server: GET /api/orders with Cookie sessionId=id
    Server->>Redis: GET sess-id
    Redis-->>Server: userId user_442, roles user
    Server->>Redis: EXPIRE sess-id 1800 reset idle timeout
    Server-->>Client: 200 orders

    %% --- Expired / missing session ---
    Note over Client,Redis: Session TTL elapses after 30 min idle
    Client->>Server: GET /api/orders with Cookie sessionId=id
    Server->>Redis: GET sess-id
    Redis-->>Server: nil
    Server-->>Client: 401 Unauthorized

    %% --- Logout ---
    Client->>Server: POST /logout
    Server->>Redis: DEL sess-id
    Server-->>Client: 200 + Clear-Cookie sessionId
```

---

## OAuth 2.0 Deep Dive

```
Roles:  Resource Owner (user), Client (your app), Auth Server (issues tokens), Resource Server (holds data)
Flow:   Client redirects user to Auth Server → user logs in + consents → Auth Server issues code
        Client exchanges code for access token → Client calls Resource Server with token
```

### Key Considerations
- **Delegated access:** The user grants your app access to their data on another service — credentials are never shared with your app
- **Authorization Code flow:** Most secure — code is exchanged server-side, access token never exposed in the browser URL
- **PKCE:** Extension for public clients (SPAs, mobile apps) that can't store a client secret — prevents code interception attacks
- **Access token:** Short-lived (minutes to hours), sent as `Authorization: Bearer <token>` to the Resource Server
- **Refresh token:** Long-lived, used to get new access tokens without re-prompting the user
- **Scopes:** Token is issued with specific permissions (e.g. `read:email`, `repo`) — Resource Server enforces these
- **State param:** Random value included in the redirect to prevent CSRF during the auth flow

### Concrete Example

**Scenario:** A user clicks "Login with Google" on your app. Your app wants to read their Google profile.

**Step 1 — Your app redirects the user to Google:**
```
GET https://accounts.google.com/o/oauth2/auth
  ?response_type=code
  &client_id=your_app_client_id
  &redirect_uri=https://yourapp.com/callback
  &scope=openid email profile
  &state=xK92mPqR4t   (random CSRF token)
```

**Step 2 — Google redirects back with an authorization code:**
```
GET https://yourapp.com/callback
  ?code=4/0AX4XfWj...
  &state=xK92mPqR4t
```

**Step 3 — Your server exchanges the code for tokens:**
```
POST https://oauth2.googleapis.com/token
  client_id=your_app_client_id
  client_secret=your_app_secret
  code=4/0AX4XfWj...
  grant_type=authorization_code
  redirect_uri=https://yourapp.com/callback

Response: {
  "access_token": "ya29.A0ARrd...",
  "expires_in": 3600,
  "refresh_token": "1//0GX...",
  "scope": "openid email profile"
}
```

**Step 4 — Your server calls the Resource Server with the token:**
```
GET https://www.googleapis.com/oauth2/v2/userinfo
Authorization: Bearer ya29.A0ARrd...

Response: { "id": "1234", "email": "alice@gmail.com", "name": "Alice" }
```

### Flow

```mermaid
sequenceDiagram
    participant User
    participant Client as Your App (Client)
    participant AuthServer as Auth Server (Google)
    participant Resource as Resource Server (Google API)

    %% --- Authorization request ---
    User->>Client: Click Login with Google
    Client->>AuthServer: Redirect with client_id, scope, state, redirect_uri
    AuthServer->>User: Show login and consent screen
    User->>AuthServer: Login and grant consent

    %% --- Code exchange ---
    AuthServer->>Client: Redirect to callback with authorization code and state
    Client->>Client: Verify state matches to prevent CSRF
    Client->>AuthServer: POST token endpoint with code and client_secret
    AuthServer-->>Client: access_token expires 1hr + refresh_token

    %% --- API call ---
    Client->>Resource: GET userinfo with Bearer access_token
    Resource->>Resource: Validate token and check scopes
    Resource-->>Client: User profile data

    %% --- Token refresh ---
    Note over Client,AuthServer: 1 hour later - access token expires
    Client->>AuthServer: POST token endpoint with refresh_token
    AuthServer-->>Client: New access_token
```

---

## OpenID Connect (OIDC) Deep Dive

```
Built on:  OAuth 2.0 (reuses the same flows and token endpoints)
Adds:      id_token (JWT) proving who the user is, not just what they can access
Use case:  "Login with Google" — authentication, not just authorization
```

### Key Considerations
- **OAuth 2.0 is not authentication:** OAuth gives you an `access_token` to call APIs, but doesn't tell you *who the user is*. OIDC fixes this.
- **ID Token:** A signed JWT returned alongside the `access_token`. Contains identity claims about the user — not for calling APIs, just for knowing who logged in.
- **`openid` scope:** Including `openid` in the OAuth request triggers OIDC — Google returns an `id_token` in addition to the `access_token`.
- **Verification:** Your server verifies the `id_token` signature using Google's public keys (published at `/.well-known/jwks.json`) — no extra network call needed.
- **UserInfo endpoint:** Alternatively, call `GET /userinfo` with the `access_token` to fetch claims — useful if you need claims not included in the token.
- **Discovery document:** OIDC providers publish metadata at `/.well-known/openid-configuration` — endpoints, supported scopes, public keys. Your app can auto-configure from this.
- **SSO:** Because identity is standardized, one OIDC provider (e.g. your company's IdP) can authenticate users across many apps — all apps trust the same `id_token` issuer.
- **OIDC vs OAuth 2.0:** OAuth answers "can this app access that resource?". OIDC answers "who is this user?". They use the same plumbing but serve different purposes.

### ID Token Structure

The `id_token` is a standard JWT with identity-specific claims:

```
Header:  { "alg": "RS256", "kid": "key-id-from-jwks" }

Payload: {
  "iss": "https://accounts.google.com",   ← who issued this token
  "sub": "1234567890",                    ← stable unique user ID (never changes)
  "aud": "your_app_client_id",            ← which app this token is for
  "exp": 1700003600,                      ← expiry (typically 1 hour)
  "iat": 1700000000,                      ← issued at
  "email": "alice@gmail.com",             ← from 'email' scope
  "name": "Alice Smith",                  ← from 'profile' scope
  "picture": "https://..."                ← from 'profile' scope
}

Signature: <RS256 signed by Google's private key>
```

**`sub` is the key field** — it's the stable identifier for the user across sessions. Email can change; `sub` never does. Use `sub` as your internal foreign key to link a Google account to a user in your DB.

### Concrete Example

**Scenario:** User clicks "Login with Google". Your app authenticates them via OIDC.

**Step 1 — Redirect to Google (same as OAuth, but `openid` scope is required):**
```
GET https://accounts.google.com/o/oauth2/auth
  ?response_type=code
  &client_id=your_app_client_id
  &redirect_uri=https://yourapp.com/callback
  &scope=openid email profile
  &state=xK92mPqR4t
```

**Step 2 — Google redirects back with an authorization code:**
```
GET https://yourapp.com/callback
  ?code=4/0AX4XfWj...
  &state=xK92mPqR4t
```

**Step 3 — Exchange code for tokens (now includes `id_token`):**
```
POST https://oauth2.googleapis.com/token
  client_id=your_app_client_id
  client_secret=your_app_secret
  code=4/0AX4XfWj...
  grant_type=authorization_code
  redirect_uri=https://yourapp.com/callback

Response: {
  "access_token": "ya29.A0ARrd...",    ← use this to call Google APIs
  "id_token":     "eyJhbGci...",       ← use this to identify the user
  "expires_in":   3600,
  "token_type":   "Bearer"
}
```

**Step 4 — Your server validates the `id_token`:**
```
1. Fetch Google's public keys from https://accounts.google.com/.well-known/jwks.json
2. Verify id_token signature using the matching key (check 'kid' header)
3. Check iss == "https://accounts.google.com"
4. Check aud == your_app_client_id  (prevents tokens issued to other apps from working here)
5. Check exp has not passed
6. Extract sub — this is your user's stable identity
```

**Step 5 — Map to your own user record:**
```
SELECT * FROM users WHERE google_sub = '1234567890'

If found  → log them in (create session or issue your own JWT)
If not    → create a new user record, then log them in
```

You never store the `id_token` itself — you extract what you need (`sub`, `email`, `name`) and use your own session mechanism from there.

### OIDC vs OAuth 2.0 Side by Side

| | OAuth 2.0 | OIDC (OAuth 2.0 + `openid`) |
|---|---|---|
| Question answered | "Can my app act on your behalf?" | "Who are you?" |
| Token returned | `access_token` | `access_token` + `id_token` |
| User identity | Not included | In `id_token` (`sub`, `email`, etc.) |
| Verify how | Call `/userinfo` API | Verify JWT signature locally |
| Use case | API authorization | Login / SSO |

### Flow

```mermaid
sequenceDiagram
    participant User
    participant Client as Your App
    participant Google as Google (OIDC Provider)

    %% --- Authorization request ---
    User->>Client: Click "Login with Google"
    Client->>Google: Redirect with scope=openid email profile + state
    Google->>User: Show login and consent screen
    User->>Google: Login and approve

    %% --- Code exchange ---
    Google->>Client: Redirect to callback with code + state
    Client->>Client: Verify state matches (CSRF check)
    Client->>Google: POST /token with code + client_secret
    Google-->>Client: access_token + id_token (JWT)

    %% --- Identity verification ---
    Client->>Google: GET /.well-known/jwks.json (fetch public keys, cached)
    Client->>Client: Verify id_token signature, iss, aud, exp
    Client->>Client: Extract sub → look up or create user in DB

    %% --- Session created ---
    Client-->>User: Logged in — issue session or app JWT
```

---

## API Key Authentication Deep Dive

```
Structure:  Long-lived opaque secret token, issued once, sent on every request
Used for:   Service-to-service, developer API access, third-party integrations
Not for:    End-user login — no identity context, no expiry by default
```

### Key Considerations
- **Opaque token:** Unlike a JWT, an API key carries no claims. The server must look it up in a store (DB, cache) on every request to find out who it belongs to and what they're allowed to do.
- **Long-lived by default:** API keys don't expire automatically — this is convenient but dangerous. A leaked key stays valid until manually revoked.
- **No user identity:** API keys identify a **client/application**, not a human user. They're suited for machine-to-machine (M2M) calls, not login flows.
- **Transmission:** Sent in the `Authorization` header (`Authorization: ApiKey <key>`), a custom header (`X-API-Key`), or as a query param (`?api_key=...`). Avoid query params — they appear in server logs and browser history.
- **Storage — client side:** Treated like a password. Never hardcode in source code; store in environment variables or a secrets manager (Vault, AWS Secrets Manager).
- **Storage — server side:** Never store the raw key. Hash it (SHA-256) and store the hash — same principle as passwords. When a request comes in, hash the incoming key and compare.
- **Scopes:** Keys should carry limited permissions (e.g. `read:data` only). A compromised key with full access is far more damaging than a scoped one.
- **Key rotation:** Support multiple active keys per client so they can rotate without downtime — generate new key, swap it in, revoke the old one.
- **Rate limiting:** Always enforce per-key rate limits. A leaked key being abused should be detectable and throttleable before it causes damage.

### Concrete Example

**Scenario:** A company exposes a REST API. Developers sign up, get an API key, and use it to query data.

**Step 1 — Key is generated at signup and shown once:**
```
POST /api/keys

Response: {
  "key_id":  "key_a1b2c3",
  "api_key": "myapp_live_9x8Kp2mQrT4nVwYzAb3cDe5f",   ← shown ONCE, never again
  "scopes":  ["read:data", "write:data"],
  "created_at": "2024-01-15T10:00:00Z"
}
```

**What the server stores in the DB (never the raw key):**
```
key_id:      key_a1b2c3
key_hash:    SHA256("myapp_live_9x8Kp2mQrT4nVwYzAb3cDe5f")  → "e3b0c44298fc..."
owner_id:    user_442
scopes:      ["read:data", "write:data"]
last_used:   null
revoked:     false
```

**Step 2 — Developer stores it in their environment:**
```bash
export API_KEY=myapp_live_9x8Kp2mQrT4nVwYzAb3cDe5f
```

**Step 3 — Developer sends it on every request:**
```
GET /api/v1/data
X-API-Key: myapp_live_9x8Kp2mQrT4nVwYzAb3cDe5f
```

**Step 4 — Server validates the key:**
```
1. Extract key from header
2. Hash the incoming key: SHA256("sk_live_9x8...") → "e3b0c44..."
3. Look up hash in DB → find key_id + owner_id + scopes
4. Check revoked == false
5. Check rate limit for this key_id (Redis: INCR key_a1b2c3:minute)
6. Check requested action is within scopes
7. Attach owner_id + scopes to request context and proceed
```

**Step 5 — Key rotation (zero downtime):**
```
1. Generate new key  → key_a1b2c3_v2 is now active alongside key_a1b2c3
2. Developer updates their env with the new key
3. Revoke old key    → key_a1b2c3 marked revoked=true
```

### Prefixing Keys (best practice)

Add a recognizable prefix so keys can be identified by secret scanners (GitHub, GitLab scan for these and alert if leaked):

```
myapp_live_9x8Kp2mQrT4nVwYzAb3cDe5f    ← live key
myapp_test_4mNqR7vLpX2wYuZcAd8eGh1j    ← test key
```

Scanners know to look for `sk_live_` and `sk_test_` patterns — GitHub will automatically alert if a developer accidentally commits one.

### API Key vs JWT

| | API Key | JWT |
|---|---|---|
| Carries claims? | No — opaque, must be looked up | Yes — self-contained |
| Expiry | None by default | Built-in (`exp`) |
| Revocation | Instant (flip DB flag) | Hard (stateless — need blocklist) |
| Server lookup on each request | Yes | No (verify signature locally) |
| Best for | M2M, developer access | User sessions, distributed systems |
| If leaked | Valid forever until revoked | Valid until expiry |

### Flow

```mermaid
sequenceDiagram
    participant Dev as Developer / Service
    participant API as Your API Server
    participant DB as Key Store (DB + Redis)

    %% --- Key issuance ---
    Dev->>API: POST /api/keys (authenticated signup)
    API->>API: Generate random key, hash it
    API->>DB: Store hash + owner_id + scopes
    API-->>Dev: Return raw key once (never stored again)

    %% --- Authenticated request ---
    Dev->>API: GET /api/v1/data\nX-API-Key: sk_live_9x8...
    API->>API: Hash incoming key
    API->>DB: Lookup hash → owner_id + scopes + revoked flag
    DB-->>API: key_a1b2c3, owner user_442, not revoked
    API->>DB: Check rate limit (Redis INCR)
    DB-->>API: Under limit
    API->>API: Verify scope covers this action
    API-->>Dev: 200 { data }

    %% --- Revocation ---
    Dev->>API: DELETE /api/keys/key_a1b2c3
    API->>DB: SET revoked=true for key_a1b2c3
    API-->>Dev: 204 No Content
    Note over Dev,DB: All future requests with this key → 401
```

---

## Session Management

- **Session fixation:** Regenerate session ID after login
- **Session timeout:** Idle timeout + absolute timeout
- **Secure flags:** `HttpOnly`, `Secure`, `SameSite`
- **Distributed sessions:** Use Redis or a shared session store for horizontal scaling

---

## Password Storage

- Never store plaintext passwords
- Use adaptive hashing algorithms: **bcrypt**, **scrypt**, **Argon2** (preferred)
- Include a **salt** to prevent rainbow table attacks
- Tune work factor as hardware improves

---

## Common Vulnerabilities

| Attack | Description | Mitigation |
|--------|-------------|------------|
| Brute Force | Repeated password guesses | Rate limiting, account lockout, CAPTCHA |
| Credential Stuffing | Leaked credentials reused | MFA, breach detection |
| Phishing | Fake login pages | FIDO2/WebAuthn, security awareness |
| Session Hijacking | Stolen session cookie | HTTPS, HttpOnly, short TTL |
| CSRF | Forged cross-site requests | CSRF tokens, SameSite cookies |
| JWT Algorithm Confusion | `alg: none` or RS→HS swap | Validate algorithm explicitly |

---

## Passwordless Authentication

- **Magic Links:** One-time login link sent to email
- **TOTP/HOTP:** Time/counter-based OTP (Google Authenticator)
- **WebAuthn / FIDO2:** Public-key cryptography via hardware key or biometrics — phishing-resistant

---

## System Design Considerations

- **Centralized Auth Service:** Single identity provider (IdP) for all services
- **Token introspection vs. local validation:** Tradeoff between freshness and latency
- **Rate limiting login endpoints:** Prevent brute force at the edge
- **Audit logging:** Record all auth events (login, logout, failures, token refresh)
- **Horizontal scaling:** Stateless tokens (JWT) scale better than sticky sessions
