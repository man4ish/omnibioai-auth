from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.core.jwt import decode_token

security = HTTPBearer()


def get_current_user(token=Depends(security)):
    try:
        return decode_token(token.credentials)
    except:
        raise HTTPException(401, "Invalid token")


def require_role(role: str):
    def wrapper(user=Depends(get_current_user)):
        if role not in user.get("roles", []):
            raise HTTPException(403, "Forbidden")
        return user
    return wrapper


def require_permission(permission: str):
    def wrapper(user=Depends(get_current_user)):
        perms = user.get("permissions", [])
        if permission not in perms:
            raise HTTPException(403, "Forbidden")
        return user
    return wrapper