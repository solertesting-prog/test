from pydantic import SecretStr

from app.api.auth import pwd_context

from .models.news import NewsArticle as NewsArticleModel
from .models.users import User as UserModel

TEST_USERNAME = "lexy"
TEST_EMAIL = "user@test.com"
TEST_PASSWORD = "password"
TEST_INTERESTS = ["technology", "business"]


async def create_db_placeholders() -> None:
    """Create placeholder users in the database."""
    await drop_placeholders()

    # Create a list of placeholder users
    test_user = await UserModel(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        interests=TEST_INTERESTS,  # type: ignore[assignment]
        password=SecretStr(pwd_context.hash(TEST_PASSWORD)),
        is_active=True,
    ).create()

    assert test_user is not None, "Failed to create test user"

    news_articles = [
        NewsArticleModel(
            title="The new PS6 is out",
            content="The new PS6 is out now :)",
            categories=["business", "technology"],
        ),
        NewsArticleModel(
            title="NASA announces new Moon mission",
            content="NASA has revealed plans for a new lunar mission set to launch in 2025, aiming to establish a sustainable human presence on the Moon.",
            categories=["science"],
        ),
        NewsArticleModel(
            title="Global markets rally after positive economic data",
            content="Stock markets worldwide saw significant gains today following the release of better-than-expected economic growth figures.",
            categories=["business"],
        ),
        NewsArticleModel(
            title="Breakthrough in cancer research offers new hope",
            content="Scientists have developed a promising new treatment that could significantly improve survival rates for certain types of cancer.",
            categories=["health", "science"],
        ),
        NewsArticleModel(
            title="Major update released for popular messaging app",
            content="The latest update introduces end-to-end encryption and several new features to enhance user privacy and experience.",
            categories=["technology"],
        ),
        NewsArticleModel(
            title="Local community garden project flourishes",
            content="Residents celebrate the success of a community garden initiative that has brought fresh produce and a sense of unity to the neighborhood.",
            categories=["lifestyle"],
        ),
    ]

    for article in news_articles:
        assert await article.create(), "Failed to create news article"
    print("Placeholder users and news articles created successfully.")


async def drop_placeholders() -> None:
    """Drop placeholder users in the database."""
    # Drop all users and news articles
    await UserModel.delete_all()
    await NewsArticleModel.delete_all()
    print("Placeholder users and news articles dropped successfully.")
