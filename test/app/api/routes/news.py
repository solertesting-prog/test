from uuid import UUID

from fastapi import APIRouter, Query, HTTPException # type: ignore

from app.core.news.entities.news_article import NewsArticle, NewsCategory, UpdateNewsArticleDto
from app.core.news.services import news_article_service
from app.core.news.services.exceptions import NewsArticleNotFound
from pydantic import BaseModel


from ..container import dependencies

router = APIRouter(
    prefix="/news",
    tags=["news"],
)
news_article_repository = dependencies().news_article_repository


@router.get("/{id}")
async def get_news_by_id(id: UUID) -> NewsArticle:
    """Get news by id."""
    try:
        news = await news_article_service.get_news_article_by_id(
            id=id, news_article_repository=news_article_repository
        )
        return news
    except NewsArticleNotFound:
        raise HTTPException(status_code=404, detail="News article not found")

import logging

# Configuración básica
logging.basicConfig(
    level=logging.INFO,  # Nivel mínimo de log que se registrará
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del mensaje
)




@router.patch("/{id}")
async def update_news_article(
    id: UUID,
    news_article:UpdateNewsArticleDto,
):
    """Update an existing news article."""
    logging.info(news_article.model_dump(exclude_unset=True))
    try:    

        updated_article = await news_article_service.update_news_article(
            id=id, news_article=UpdateNewsArticleDto(**news_article.model_dump()), news_article_repository=news_article_repository
        )
        return updated_article
    except NewsArticleNotFound:
        raise HTTPException(status_code=404, detail="News article not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))





@router.get("/")
async def get_news(
    category: NewsCategory | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[NewsArticle]:
    """Get all news articles."""
    news = await news_article_service.get_all_news_articles(
        news_article_repository, skip=skip, limit=limit, category=category
    )
    return news
