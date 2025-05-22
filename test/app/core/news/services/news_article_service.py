from typing import List
from uuid import UUID


from ..entities.news_article import NewsArticle, NewsCategory, UpdateNewsArticleDto
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
    category: NewsCategory | None = None,
) -> List[NewsArticle]:
    """Fetch all news articles with pagination."""
    return await news_article_repository.fetch_all_by_category(
        category=category, limit=limit, skip=skip
    )

async def update_news_article(
    news_article_repository: NewsArticleRepository,
    id:UUID ,
    news_article: UpdateNewsArticleDto
) -> NewsArticle:

   news_article_updated= await news_article_repository.update(
        dto=news_article,id=id
    )
   if not news_article_updated:
        raise NewsArticleNotFound(article_id=id)
   return news_article_updated



async def remove_news_article(
    news_article_repository: NewsArticleRepository,
    id:UUID ,
) -> NewsArticle:

    deleted_article = await news_article_repository.remove(id=id)
    if not deleted_article:
        raise NewsArticleNotFound(article_id=id)
    return deleted_article