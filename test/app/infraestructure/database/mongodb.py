from beanie import init_beanie as __init_beanie
from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

from .models import __beanie_models__

type AsyncMongoClient = AsyncMongoMockClient | AsyncIOMotorClient


def init_db_dev_connection() -> AsyncMongoClient:
    if settings.testing:
        return init_test_connection()

    return AsyncIOMotorClient(
        str(settings.database_local_url),
    )


async def init_beanie(
    database_client: AsyncMongoClient,
) -> None:
    """Initialize beanie with the database client and the models"""

    await __init_beanie(
        database_client[settings.database_name], document_models=__beanie_models__  # type: ignore
    )


def init_test_connection() -> AsyncMongoMockClient:
    return AsyncMongoMockClient(
        str(settings.database_local_url),
    )
