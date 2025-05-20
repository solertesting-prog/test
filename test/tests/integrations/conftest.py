"""
Pytest fixtures
"""

from typing import Iterator

import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.config import settings
from app.infraestructure.database.seed import TEST_PASSWORD, TEST_USERNAME

settings.testing = True


@pytest.fixture(scope="session")
def test_client() -> Iterator[TestClient]:
    """Fixture to mock the motor client."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def bearer_token(test_client: TestClient) -> str:
    """Fixture to provide a bearer token for authentication."""
    response = test_client.post(
        "/users/auth",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        },
    )
    assert response.status_code == 200, "Failed to authenticate user"
    return response.json()["access_token"]
