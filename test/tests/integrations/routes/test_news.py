import random
from typing import get_args
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from app.core.news.entities.news_article import NewsCategory

@pytest.fixture
def news_id(test_client: TestClient, bearer_token: str) -> str:
    """Fixture to get the ID of a random news article."""
    response = test_client.get(
        "/news",
        headers={"Authorization": f"Bearer {bearer_token}"},
        params={"skip": 0, "limit": 10},
    )
    assert response.status_code == 200, "Failed to fetch news articles"
    news_articles = response.json()
    assert len(news_articles) > 0, "No news articles found"
    random_article = random.choice(news_articles) 
    return random_article["id"]  

@pytest.mark.order(1)
async def test_get_news_by_user_interests(test_client: TestClient, bearer_token: str) -> None:
    """Test that the /news/user-interests endpoint returns news based on user interests."""
    response = test_client.get(
        "/news/user-interests",
        headers={"Authorization": f"Bearer {bearer_token}"},
        params={"skip": 0, "limit": 10},
    )
    if response.status_code == 404:
        assert response.json()["detail"] == "No interests found for the user."
    else:
        assert response.status_code == 200
        assert isinstance(response.json(), list), "Response should be a list of news articles"


@pytest.mark.order(2)
async def test_get_news_by_id(test_client: TestClient, news_id: str, bearer_token: str) -> None:
    """Test that the /news/{id} endpoint retrieves a news article by ID."""
    response = test_client.get(
        f"/news/{news_id}",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )
    if response.status_code == 404:
        assert response.json()["detail"] == "News article not found"
    else:
        assert response.status_code == 200
        assert "id" in response.json(), "Response should contain the news article ID"


@pytest.mark.order(3)
async def test_update_news_article(test_client: TestClient, news_id: str, bearer_token: str) -> None:
    """Test that the /news/{id} endpoint updates a news article."""
    update_data = {
        "title": "Updated Title",
        "content": "Updated Content",
    }
    response = test_client.patch(
        f"/news/{news_id}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json=update_data,
    )
    if response.status_code == 404:
        assert response.json()["detail"] == "News article not found"
    else:
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        assert response.json()["content"] == "Updated Content"


@pytest.mark.order(4)
async def test_delete_news_article(test_client: TestClient, news_id: str, bearer_token: str) -> None:
    """Test that the /news/{id} endpoint deletes a news article."""
    response = test_client.delete(
        f"/news/{news_id}",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )
    if response.status_code == 404:
        assert response.json()["detail"] == "News article not found"
    else:
        assert response.status_code == 200
        assert response.json()["message"] == "News article removed successfully"


@pytest.mark.order(5)
def test_create_news_article(test_client: TestClient, bearer_token: str) -> None:
    """Test that the /news/ endpoint creates a new news article."""
    payload = {
        "title": "Breaking News",
        "content": "This is the content of the news article.",
        "categories": ["sports"],
    }

    response = test_client.post(
        "/news/",
        headers={"Authorization": f"Bearer {bearer_token}"},
        json=payload,
    )

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    data = response.json()

    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["categories"] == payload["categories"]
    assert "id" in data, "The response should contain an 'id' field"