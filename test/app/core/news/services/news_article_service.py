from typing import List
from uuid import UUID

from ..entities.news_article import NewsArticle, NewsCategory
from ..protocols.news_repository import NewsArticleRepository
from .exceptions import NewsArticleNotFound


async def get_news_article_by_id(
    news_article_repository: NewsArticleRepository, id: UUID
) -> NewsArticle:
    """Fetch a news article by its ID."""
    news_article = await news_article_repository.fetch_by_id(id)
    if not news_article:
        raise NewsArticleNotFound(article_id=id)
    return news_article


async def get_all_news_articles(
    news_article_repository: NewsArticleRepository,
    skip: int = 0,
    limit: int = 100,
) -> List[NewsArticle]:
    """Fetch all news articles with pagination."""
    # TODO: Implement pagination logic
    raise NotImplementedError("Fetching all news articles is not implemented yet.")


async def get_news_articles_by_category(
    news_article_repository: NewsArticleRepository,
    category: NewsCategory,
    skip: int = 0,
    limit: int = 100,
) -> List[NewsArticle]:
    """Fetch news articles by category with pagination."""
    raise NotImplementedError("Fetching news articles by category is not implemented yet.")
