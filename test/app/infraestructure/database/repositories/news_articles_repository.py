# TODO: implement all missing methods
from typing import List, Optional
from uuid import UUID

from app.core.news.entities.news_article import (
    CreateNewsArticleDto,
    NewsArticle,
    NewsCategory,
    UpdateNewsArticleDto,
)

from ..models.news import NewsArticle as NewsArticleModel


async def create(dto: CreateNewsArticleDto) -> NewsArticle:
    """Create a new news article in the database.

    Args:
        dto (CreateNewsArticleDto): The data transfer object containing news article details.
    """
    news_article = await NewsArticleModel(**dto.model_dump()).insert()
    return NewsArticle(**news_article.model_dump())


async def fetch_by_id(id: UUID) -> Optional[NewsArticle]:
    """Fetch a news article by ID from the database.

    Args:
        id (UUID): The ID of the news article to retrieve.
    """
    news_article = await NewsArticleModel.get(id)
    if not news_article:
        return None

    return NewsArticle(**news_article.model_dump())


async def fetch_all_by_category(
    category: NewsCategory, limit: int, skip: int
) -> List[NewsArticle]:
    raise NotImplementedError(
        "Fetching news articles by category is not implemented yet."
    )


async def update(id: UUID, dto: UpdateNewsArticleDto) -> Optional[NewsArticle]:
    raise NotImplementedError("Updating news articles is not implemented yet.")


async def remove(id: UUID) -> NewsArticle:
    raise NotImplementedError("Removing news articles is not implemented yet.")
