from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from ..infraestructure.database.mongodb import init_beanie, init_db_dev_connection
from ..infraestructure.database.seed import create_db_placeholders
from .routes import build_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the application.

    Args:
        app (FastAPI): FastAPI application instance
    """
    # Initialize the database connection
    database_client = init_db_dev_connection()
    await init_beanie(database_client)
    await create_db_placeholders()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Backend API",
    description="Backend API for the application",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users",
        },
        {
            "name": "news",
            "description": "Operations with news",
        },
    ],
)

# Build the routers
build_routers(app)

# CORS middleware(for Testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint


@app.get("/", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "API is running! :)"}
