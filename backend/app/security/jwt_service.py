from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from backend.app.core.config import settings

class JWTService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
            
        to_encode.update({
            "exp": expire,
            "iss": settings.token_issuer,
            "aud": settings.token_audience
        })
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token, 
                settings.secret_key, 
                algorithms=[settings.algorithm],
                audience=settings.token_audience,
                issuer=settings.token_issuer
            )
            return payload
        except JWTError:
            return None
