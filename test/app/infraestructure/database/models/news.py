from typing import List
from uuid import UUID, uuid4
from beanie import Document


from pydantic import Field

from datetime import datetime, timezone

from app.core.news.entities.news_article import NewsCategory

class NewsArticle(Document):
    id: UUID= Field(default_factory=uuid4)
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=255)
    categories: List[NewsCategory] = Field(..., max_length=10)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)

    class Settings:
        name = "news_articles"
