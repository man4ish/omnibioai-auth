from app.db.models import User
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token


def authenticate_user(db, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def generate_tokens(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "roles": [r.name for r in user.roles],
    }

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
    }