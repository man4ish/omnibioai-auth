import pytest
from fastapi import HTTPException

from app.rbac import require_role, require_permission


def make_user(roles=None, permissions=None):
    return {
        "sub": "123",
        "email": "test@test.com",
        "roles": roles or [],
        "permissions": permissions or [],
    }


# require_role / require_permission return a FastAPI dependency function.
# Calling it with an explicit `user=` kwarg bypasses the Depends and lets
# us unit-test the authorization logic without a running server.

# ── require_role ──────────────────────────────────────────────────────────────

def test_require_role_passes_with_correct_role():
    user = make_user(roles=["admin"])
    checker = require_role("admin")
    result = checker(user=user)
    assert result == user


def test_require_role_fails_with_wrong_role():
    user = make_user(roles=["user"])
    checker = require_role("admin")
    with pytest.raises(HTTPException) as exc:
        checker(user=user)
    assert exc.value.status_code == 403


def test_require_role_fails_with_no_roles():
    user = make_user(roles=[])
    checker = require_role("admin")
    with pytest.raises(HTTPException) as exc:
        checker(user=user)
    assert exc.value.status_code == 403


def test_require_role_passes_when_user_has_multiple_roles():
    user = make_user(roles=["user", "admin", "researcher"])
    checker = require_role("researcher")
    result = checker(user=user)
    assert result == user


# ── require_permission ────────────────────────────────────────────────────────

def test_require_permission_passes():
    user = make_user(permissions=["read:samples"])
    checker = require_permission("read:samples")
    result = checker(user=user)
    assert result == user


def test_require_permission_fails():
    user = make_user(permissions=["read:samples"])
    checker = require_permission("write:samples")
    with pytest.raises(HTTPException) as exc:
        checker(user=user)
    assert exc.value.status_code == 403


def test_require_permission_fails_with_no_permissions():
    user = make_user(permissions=[])
    checker = require_permission("read:samples")
    with pytest.raises(HTTPException) as exc:
        checker(user=user)
    assert exc.value.status_code == 403
