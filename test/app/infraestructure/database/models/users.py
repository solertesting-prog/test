from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field, SecretStr

from app.core.users.entities.user import UserInterests


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    username: Annotated[str, Indexed(unique=True)] = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    password: SecretStr
    interests: list[UserInterests] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)

    class Settings:
        name = "users"
