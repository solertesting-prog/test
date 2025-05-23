from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException

from app.core.news.entities.news_article import NewsArticle, NewsCategory, UpdateNewsArticleDto,CreateNewsArticleDto
from app.core.news.services import news_article_service
from app.core.news.services.exceptions import NewsArticleNotFound
from pydantic import BaseModel


from app.core.users.services import user_service
from app.core.users.entities.user import UserRegistry


from ..container import dependencies, get_current_user

user_repository = dependencies().user_repository

router = APIRouter(
    prefix="/news",
    tags=["news"],
    dependencies=[Depends(get_current_user)], 
)
news_article_repository = dependencies().news_article_repository


@router.get("/user-interests")
async def get_news_by_user_interests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user: UserRegistry = Depends(get_current_user),
) -> list[NewsArticle]:
    """Get news articles based on the user's interests."""
    logging.info(user)

    try:
        user_data = await user_service.get_user_by_id(
        user_repository=user_repository,
        user=user,
    )
        user_interests = user_data.interests

        if not user_interests:
            raise HTTPException(status_code=404, detail="No interests found for the user.")

        # Obtener las noticias basadas en los intereses del usuario
        news = await news_article_service.get_all_news_articles(
            category=[interest for interest in user_interests],
            news_article_repository=news_article_repository,
            skip=skip,
            limit=limit,
        )

        return news
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
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



@router.delete("/{id}")
async def delete_news_article(id: UUID):
    """Delete a news article by its ID."""
    try:
        # Lógica para eliminar el artículo
        deleted_article = await news_article_service.remove_news_article(id=id, news_article_repository=news_article_repository) # type: ignore
        if not deleted_article:
            raise HTTPException(status_code=404, detail="News article not found")
        return {"message": "News article removed successfully"}
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

@router.post("/")
async def create_news_article(
    news_article: CreateNewsArticleDto,
) -> NewsArticle:
    """Create a new news article."""
    try:
        
        created_article = await news_article_service.create_news_article(
            news_article=CreateNewsArticleDto(**news_article.model_dump()),
            news_article_repository=news_article_repository,
        )
        return created_article
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))