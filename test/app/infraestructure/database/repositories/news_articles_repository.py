# TODO: implement all missing methods
from typing import List, Optional
from uuid import UUID
import logging


# Configuración básica
logging.basicConfig(
    level=logging.INFO,  # Nivel mínimo de log que se registrará
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del mensaje
)

from app.core.news.entities.news_article import (
    CreateNewsArticleDto,
    NewsArticle,
    NewsCategory,
    UpdateNewsArticleDto
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
    category: Optional[NewsCategory], limit: int, skip: int
) -> List[NewsArticle]:
    if category:
        articles = (
            await NewsArticleModel.find(NewsArticleModel.categories == category)
            .skip(skip)
            .limit(limit)
            .to_list()
        )
    else:
        articles = await NewsArticleModel.find().skip(skip).limit(limit).to_list()
 
    if not articles:
        return []
    return [NewsArticle(**article.model_dump()) for article in articles]


async def update(id: UUID, dto: UpdateNewsArticleDto) -> Optional[NewsArticle]:
    news_article = await NewsArticleModel.get(id)
    if not news_article:
        return None
    logging.info(dto.model_dump(exclude_unset=True))

    await news_article.set(dto.model_dump(exclude_unset=True)) 

    logging.info(news_article)

    return NewsArticle(**news_article.model_dump())


async def remove(id: UUID) -> NewsArticle:
    raise NotImplementedError("Removing news articles is not implemented yet.")
