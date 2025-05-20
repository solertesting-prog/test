from datetime import datetime, timezone
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

NewsCategory = Literal[
    "sports",
    "technology",
    "business",
    "science",
    "health",
    "entertainment",
    "politics",
    "world",
    "lifestyle",
    "education",
    "travel",
    "food",
    "fashion",
]


class NewsArticle(BaseModel):
    id: UUID = Field(default_factory=UUID)
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=5000)
    categories: List[NewsCategory] = Field(..., max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CreateNewsArticleDto(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=5000)


class UpdateNewsArticleDto(BaseModel): ...
