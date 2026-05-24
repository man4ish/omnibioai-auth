from app.db.models import RevokedToken
from app.core.jwt import decode_token


def is_token_revoked(db, jti: str) -> bool:
    return db.query(RevokedToken).filter(
        RevokedToken.token_jti == jti
    ).first() is not None


def revoke_token(db, token_payload):
    jti = token_payload.get("jti")

    if jti:
        db.add(RevokedToken(token_jti=jti))
        db.commit()