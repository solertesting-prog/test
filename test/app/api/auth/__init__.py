from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field, SecretStr

from app.config import settings
from app.core.users.entities.user import UserRegistry

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class UserTokenData(BaseModel):
    """Data model for user token data."""

    exp: datetime = Field(..., description="Expiration time of the token")
    iat: datetime = Field(..., description="Issued at time of the token")
    sub: UUID = Field(..., description="Subject of the token")


def verify_password(plain_password: SecretStr, hashed_password: SecretStr) -> bool:
    return pwd_context.verify(
        plain_password.get_secret_value(), hashed_password.get_secret_value()
    )


def get_password_hash(password: SecretStr) -> SecretStr:
    return SecretStr(pwd_context.hash(password.get_secret_value()))


def create_access_token(user_registry: UserRegistry) -> str:
    """Create a JWT access token for the user.
    Args:
        user_registry (UserRegistry): The user registry instance.
    Returns:
        str: The encoded JWT token.
    """
    to_encode = {
        "sub": user_registry.id,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        "iat": datetime.now(tz=timezone.utc),
    }
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)

    return encoded_jwt


def decode_access_token(token: str) -> UserTokenData:
    """Decode the JWT access token.
    Args:
        token (str): The JWT token to decode.
    Returns:
        UserTokenData: The decoded token payload.
    """
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return UserTokenData(**payload)
