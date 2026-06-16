# omnibioai-auth

**JWT authentication and authorization service for the OmniBioAI platform.**

Central identity layer for the OmniBioAI zero-trust security plane.
Handles user registration, login, token issuance, refresh, logout,
and validation across all platform services.

---

## Architecture Role

`omnibioai-auth` runs as a containerized service inside the OmniBioAI Docker
Compose stack. All platform services — TES (workflow execution), Studio
(Electron UI), LIMS (data management), and Control Center — delegate token
validation to this service rather than implementing their own auth logic.

```
Studio / TES / LIMS / Control Center / SDK
              |
        POST /auth/validate
              |
       omnibioai-auth (:8001)
         /         \
      MySQL        Redis
  (users, tokens)  (blacklist, pub/sub)
```

Redis also carries a `policy:invalidate` pub/sub channel. On logout,
`omnibioai-auth` publishes an invalidation event so downstream services can
flush any cached token state immediately.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/auth/register` | Create a new user account |
| `POST` | `/auth/login` | Authenticate and issue access + refresh tokens |
| `POST` | `/auth/refresh` | Exchange a valid refresh token for a new access token |
| `POST` | `/auth/logout` | Revoke refresh token; blacklist access token in Redis |
| `POST` | `/auth/validate` | Validate a token and return user identity + roles |
| `GET`  | `/health` | Liveness check — returns `{"status": "ok"}` |
| `GET`  | `/metrics` | Prometheus metrics (jwt_auth_total counter) |

### Login

```http
POST /auth/login
Content-Type: application/json

{"email": "user@example.com", "password": "..."}
```

```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer"
}
```

### Validate

```http
POST /auth/validate
Content-Type: application/json

{"token": "<jwt>"}
```

```json
{
  "valid": true,
  "user_id": 1,
  "email": "user@example.com",
  "roles": ["researcher"],
  "permissions": ["workflow:run", "dataset:read"]
}
```

---

## Token Model

- **Access token** — HS256 JWT, 15-minute TTL. On logout, the JTI is written
  to Redis with a matching TTL so the token is immediately rejected by
  `/auth/validate` for the rest of its natural lifetime.
- **Refresh token** — HS256 JWT, 7-day TTL. Stored in MySQL; revoked in the
  `revoked_tokens` table on logout or explicit revocation.
- **Validation fast path** — Redis blacklist checked before the DB query.

---

## RBAC

Roles and permissions are embedded in the JWT payload and enforced by
`app/rbac.py` via FastAPI dependency injection.

**Roles:** `admin`, `researcher`, `hpc_user`, `viewer`

**Permissions:** `workflow:run`, `workflow:cancel`, `dataset:read`,
`dataset:write`, `hpc:submit`

---

## Running in the Stack

This service is not intended to run in isolation. Start it via the top-level
`docker-compose.yml` in the `machine/` monorepo:

```bash
docker compose up omnibioai-auth
```

The service depends on `mysql` and `redis` compose services being healthy
before it starts. An admin user is bootstrapped automatically on first startup.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_USER` | — | MySQL username |
| `DB_PASSWORD` | — | MySQL password |
| `DB_HOST` | `localhost` | MySQL host (use `mysql` inside compose) |
| `DB_PORT` | `3306` | MySQL port |
| `DB_NAME` | `omnibioai` | Database name |
| `SECRET_KEY` | — | JWT signing secret (required) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime |
| `REDIS_URL` | `redis://redis:6379` | Redis connection URL |

---

## Project Structure

```
app/
├── main.py                  # FastAPI entrypoint, admin bootstrap, /metrics, /health
├── rbac.py                  # Role + permission dependency helpers
├── api/
│   ├── routes_auth.py       # Auth endpoints + Redis blacklist logic
│   └── deps.py              # Shared FastAPI dependencies
├── core/
│   ├── config.py            # Settings from environment
│   ├── jwt.py               # Token creation and decoding
│   └── security.py          # Password hashing
├── db/
│   ├── models.py            # User, RefreshToken, RevokedToken models
│   ├── session.py           # SQLAlchemy engine + session factory
│   ├── base.py              # Declarative base
│   └── init_admin.py        # Admin user bootstrap
├── services/
│   ├── auth_service.py      # authenticate, generate_tokens, revoke_token
│   ├── user_service.py      # User CRUD helpers
│   └── service_tokens.py    # Service-to-service token helpers
└── schemas/
    ├── auth.py              # LoginRequest, RefreshRequest, LogoutRequest
    └── user.py              # User response schemas
```

---

## Tests

```bash
pytest tests/
```

Coverage targets: auth flows (`test_auth.py`), RBAC (`test_rbac.py`),
security primitives (`test_security.py`), health check (`test_health.py`).
