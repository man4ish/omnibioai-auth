from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

import uuid

def create_access_token(data: dict):
    to_encode = data.copy()

    to_encode.update({
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "type": "access",
        "jti": str(uuid.uuid4())   # 👈 IMPORTANT
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)    


def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + timedelta(days=7),
        "type": "refresh"
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

