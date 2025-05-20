from dataclasses import dataclass
from typing import Annotated, Callable, cast

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

# Protocols
from app.core.news.protocols.news_repository import NewsArticleRepository
from app.core.users.entities.user import UserRegistry
from app.core.users.protocols.user_repository import UserRepository

# Implementations
from app.infraestructure.database.repositories import (
    news_articles_repository,
    user_repository,
)

from .auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")


@dataclass(frozen=True)
class Dependencies:
    """Dependency container for the application."""

    user_repository: UserRepository
    news_article_repository: NewsArticleRepository


def _build_dependencies() -> Callable[[], Dependencies]:
    """Build the dependency container for the application.

    Returns:
        Callable[[], Dependencies]: Dependency container
    """
    deps = Dependencies(
        user_repository=cast(UserRepository, user_repository),
        news_article_repository=cast(NewsArticleRepository, news_articles_repository),
    )

    def fn() -> Dependencies:
        return deps

    return fn


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserRegistry:
    """Get the current user from the token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        UserRegistry: The user registry instance.
    """
    # TODO: When the token is expired, it should return a 401 error
    payload = decode_access_token(token)
    return UserRegistry(id=payload.sub)


dependencies = _build_dependencies()
