from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, SecretStr, model_validator
from pydantic.networks import EmailStr

UserInterests = Literal[
    "sports",
    "technology",
    "business",
    "science",
]


class User(BaseModel):
    id: UUID = Field(default_factory=UUID)
    username: str = Field(..., max_length=255)
    password: SecretStr
    email: str = Field(..., max_length=255)
    interests: list[UserInterests] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CreateUserDto(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr = Field(..., max_length=255)
    interests: list[UserInterests] = Field(default_factory=list)
    password: SecretStr = Field(..., min_length=8, max_length=28)


class UserRegistry(BaseModel):
    id: UUID = Field(default_factory=UUID)
