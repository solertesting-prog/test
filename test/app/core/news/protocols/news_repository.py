from ..entities.news_article import NewsArticle, UpdateNewsArticleDto, NewsCategory
from typing import List, Optional, Protocol

from uuid import UUID



class NewsArticleRepository(Protocol):
    """Protocol for news article repository.

    This protocol defines the methods that a news article repository should implement.
    """

    async def create(self, dto: NewsArticle) -> NewsArticle:
        """Create a new news article in the database.

        Args:
            dto (NewsArticle): The data transfer object containing news article details.
        """
        ...

    async def fetch_by_id(self, id: UUID) -> Optional[NewsArticle]:
        """Fetch a news article by ID from the database.

        Args:
            id (UUID): The ID of the news article to retrieve.
        """
        ...
    
    async def fetch_all_by_category(self, category: NewsCategory, limit: int, skip: int) -> List[NewsArticle]:
        """Fetch news articles by category from the database.

        Args:
            category (NewsCategory): The category of the news article to retrieve.
            limit (int): The maximum number of news articles to retrieve.
            skip (int): The number of news articles to skip.
        """
        ...

    async def update(self, id: UUID, dto: UpdateNewsArticleDto) -> Optional[NewsArticle]:
        """Update an existing news article in the database.

        Args:
            id (UUID): The ID of the news article to update.
            dto (UpdateNewsArticleDto): The data transfer object containing updated news article details.
        """
        ...