import time
import jwt
from typing import List


class ServiceTokenIssuer:
    def __init__(self, secret: str):
        self.secret = secret

    def issue_token(
        self,
        service_name: str,
        allowed_aud: List[str],
        ttl_seconds: int = 300,
    ):
        payload = {
            "type": "service",
            "service": service_name,
            "aud": allowed_aud,
            "iat": int(time.time()),
            "exp": int(time.time()) + ttl_seconds,
        }

        return jwt.encode(payload, self.secret, algorithm="HS256")