import pytest


# ── Register ──────────────────────────────────────────────────────────────────

def test_register_new_user(client):
    resp = client.post(
        "/auth/register",
        json={"email": "newuser@test.com", "password": "Password123!"},
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "User created"


def test_register_duplicate_user(client):
    client.post(
        "/auth/register",
        json={"email": "dup@test.com", "password": "Password123!"},
    )
    resp = client.post(
        "/auth/register",
        json={"email": "dup@test.com", "password": "Password123!"},
    )
    assert resp.status_code == 400
    assert "already exists" in resp.json()["detail"]


# ── Login ─────────────────────────────────────────────────────────────────────

def test_login_success(client, registered_user):
    resp = client.post("/auth/login", json=registered_user)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    resp = client.post(
        "/auth/login",
        json={"email": registered_user["email"], "password": "wrongpassword"},
    )
    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post(
        "/auth/login",
        json={"email": "nobody@test.com", "password": "password"},
    )
    assert resp.status_code == 401


def test_login_missing_fields(client):
    resp = client.post("/auth/login", json={})
    assert resp.status_code == 422


# ── Validate ──────────────────────────────────────────────────────────────────

def test_validate_valid_token(client, auth_tokens):
    resp = client.post("/auth/validate", json={"token": auth_tokens["access_token"]})
    assert resp.status_code == 200
    data = resp.json()
    assert data["valid"] is True
    assert "user_id" in data
    assert "email" in data


def test_validate_invalid_token(client):
    resp = client.post("/auth/validate", json={"token": "not.a.valid.token"})
    assert resp.status_code == 200
    assert resp.json()["valid"] is False


def test_validate_empty_token(client):
    resp = client.post("/auth/validate", json={"token": ""})
    assert resp.status_code == 200
    assert resp.json()["valid"] is False


def test_validate_missing_token_key(client):
    # req.get("token") returns None → decode raises → {"valid": False}
    resp = client.post("/auth/validate", json={})
    assert resp.status_code == 200
    assert resp.json()["valid"] is False


# ── Refresh ───────────────────────────────────────────────────────────────────

def test_refresh_valid_token(client, auth_tokens):
    resp = client.post(
        "/auth/refresh",
        json={"refresh_token": auth_tokens["refresh_token"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    # Implementation echoes back the same refresh token
    assert data["refresh_token"] == auth_tokens["refresh_token"]


def test_refresh_invalid_token(client):
    resp = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid.token.here"},
    )
    assert resp.status_code == 401


# ── Logout ────────────────────────────────────────────────────────────────────

def test_logout(client, auth_tokens):
    resp = client.post(
        "/auth/logout",
        json={"refresh_token": auth_tokens["refresh_token"]},
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "Logged out"


def test_refresh_fails_after_logout(client, registered_user):
    """After logout the refresh token is revoked; new access tokens cannot be issued."""
    login_resp = client.post("/auth/login", json=registered_user)
    tokens = login_resp.json()

    client.post("/auth/logout", json={"refresh_token": tokens["refresh_token"]})

    # Refresh must be rejected once the refresh_token row is revoked
    refresh_resp = client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert refresh_resp.status_code == 401


def test_access_token_still_valid_after_logout(client, registered_user):
    """Short-lived access tokens remain valid after logout.

    The implementation revokes the refresh_token row but does not insert
    the access token's JTI into revoked_tokens.  Validate checks only that
    table, so the access token is still accepted until it expires.
    """
    login_resp = client.post("/auth/login", json=registered_user)
    tokens = login_resp.json()

    client.post("/auth/logout", json={"refresh_token": tokens["refresh_token"]})

    validate_resp = client.post(
        "/auth/validate", json={"token": tokens["access_token"]}
    )
    assert validate_resp.json()["valid"] is True
