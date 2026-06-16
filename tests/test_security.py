import pytest
from jose import JWTError

from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token


# ── Password hashing ──────────────────────────────────────────────────────────

def test_hash_password_produces_hash():
    h = hash_password("mysecret")
    assert h != "mysecret"
    assert len(h) > 20


def test_verify_correct_password():
    h = hash_password("mysecret")
    assert verify_password("mysecret", h) is True


def test_verify_wrong_password():
    h = hash_password("mysecret")
    assert verify_password("wrongpassword", h) is False


def test_hash_is_unique():
    # bcrypt embeds a random salt, so two hashes of the same input differ
    h1 = hash_password("mysecret")
    h2 = hash_password("mysecret")
    assert h1 != h2


# ── JWT ───────────────────────────────────────────────────────────────────────

def test_create_and_decode_access_token():
    payload = {"sub": "123", "email": "test@test.com", "roles": ["user"]}
    token = create_access_token(payload)
    decoded = decode_token(token)
    assert decoded["sub"] == "123"
    assert decoded["email"] == "test@test.com"
    assert decoded["type"] == "access"
    assert "jti" in decoded
    assert "exp" in decoded


def test_create_and_decode_refresh_token():
    payload = {"sub": "123"}
    token = create_refresh_token(payload)
    decoded = decode_token(token)
    assert decoded["sub"] == "123"
    assert decoded["type"] == "refresh"


def test_access_token_has_unique_jti():
    payload = {"sub": "123"}
    t1 = create_access_token(payload)
    t2 = create_access_token(payload)
    d1 = decode_token(t1)
    d2 = decode_token(t2)
    assert d1["jti"] != d2["jti"]


def test_decode_invalid_token_raises():
    with pytest.raises(Exception):
        decode_token("not.a.real.token")
