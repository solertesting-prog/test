from typing import Literal

from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ALLOWED_ALGORITHMS = Literal["HS256",]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
    )
    # Secret key for JWT encoding and decoding
    secret_key: str = Field(..., pattern=r"^[a-zA-Z0-9_]{32,}$")
    algorithm: ALLOWED_ALGORITHMS = Field(...)
    access_token_expire_minutes: int = Field(..., gt=0)
    # Database connection string
    database_local_url: MongoDsn = Field(...)
    database_name: str = Field(..., min_length=1)
    testing: bool = Field(False)


settings = Settings()  # type: ignore[call-arg]
