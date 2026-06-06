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

## OAuth 2.0 Authorization Code Flow

```
User → Client → Authorization Server (login + consent)
             ← Authorization Code
Client → Authorization Server (code + client secret)
       ← Access Token + Refresh Token
Client → Resource Server (Access Token)
       ← Protected Resource
```

**PKCE (Proof Key for Code Exchange):** Extension for public clients (SPAs, mobile) to prevent code interception attacks.

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
