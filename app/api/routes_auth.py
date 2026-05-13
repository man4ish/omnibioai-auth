from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.services.auth_service import authenticate_user, generate_tokens
from app.core.jwt import decode_token, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):

    user = authenticate_user(db, req.email, req.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return generate_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(req: RefreshRequest):

    payload = decode_token(req.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token(payload)

    return {
        "access_token": new_access,
        "refresh_token": req.refresh_token,
        "token_type": "bearer",
    }