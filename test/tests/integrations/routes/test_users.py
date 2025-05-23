import random
from typing import get_args
from fastapi.testclient import TestClient
import pytest

from app.infraestructure.database.seed import (
    TEST_EMAIL,
    TEST_INTERESTS,
    TEST_PASSWORD,
    TEST_USERNAME,
)
from app.core.users.entities.user import UserInterests

@pytest.mark.order(0)
async def test_unregistered_user(test_client: TestClient) -> None:
    """Test that the /users/me endpoint returns a 401 for an unregistered user."""
    response = test_client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

@pytest.mark.order(1)
async def test_auth_user(test_client: TestClient) -> None:
    """Test that the /users/auth endpoint returns a token for valid credentials."""
    response = test_client.post(
        "/users/auth",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        },
    )
    assert response.status_code == 200
    assert response.json(), "Failed to authenticate user"
    assert response.json()["access_token"], "No access token returned"
    assert response.json()["token_type"] == "bearer"

@pytest.mark.order(2)
async def test_auth_user_invalid_credentials(test_client: TestClient) -> None:
    """Test that the /users/auth endpoint returns a 401 for invalid credentials."""
    response = test_client.post(
        "/users/auth",
        data={
            "username": TEST_USERNAME,
            "password": "wrong_password",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


@pytest.mark.order(3)
async def test_get_user_info(test_client: TestClient, bearer_token: str) -> None:
    """Test that the /users/me endpoint returns a placeholder response."""
    response = test_client.get(
        "/users/me", headers={"Authorization": f"Bearer {bearer_token}"}
    )
    assert response.status_code == 200
    assert response.json(), "Failed to get user info"
    assert response.json()["username"] == TEST_USERNAME
    assert response.json()["email"] == TEST_EMAIL
    assert response.json()["interests"] == TEST_INTERESTS


@pytest.mark.order(4)
@pytest.fixture
def user_id(test_client: TestClient, bearer_token: str) -> str:
    """Fixture to get the user ID from the /users/me endpoint."""
    response = test_client.get(
        "/users/me", headers={"Authorization": f"Bearer {bearer_token}"}
    )
    assert response.status_code == 200, "Failed to get user info"
    return response.json()["id"]


@pytest.mark.order(5)
def test_get_user_interests(test_client: TestClient, user_id: str) -> None:
    """Test that the /users/{user_id}/interests endpoint retrieves user interests."""
    response = test_client.get(f"/users/{user_id}/interests")
    if response.status_code == 404:
        assert response.json()["detail"] == "User not found"
    else:
        assert response.status_code == 200
        assert response.json()["message"] == "User interests retrieved successfully"
        assert response.json()["interests"] == TEST_INTERESTS


@pytest.mark.order(6)
def test_add_and_delete_user_interest(test_client: TestClient, user_id: str) -> None:
    """Test adding and deleting a user interest."""
    all_interests = get_args(UserInterests)
    new_interest: UserInterests = random.choice(all_interests)

    response = test_client.post(f"/users/{user_id}/interests/{new_interest}")
    if response.status_code == 400:
     return

    if response.status_code == 404:
        assert response.json()["detail"] == "User not found"
    else:
        assert response.status_code == 200
        assert response.json()["message"] == "Interest added successfully"
        assert new_interest in response.json()["user"]["interests"]

    response = test_client.delete(f"/users/{user_id}/interests/{new_interest}")
    if response.status_code == 404:
        assert response.json()["detail"] == "User not found"
    else:
        assert response.status_code == 200
        assert response.json()["message"] == "Interest removed successfully"
        assert new_interest not in response.json()["user"]["interests"]

@pytest.mark.order(7)
def test_delete_user(test_client: TestClient, user_id: str) -> None:
    """Test that the /users/{user_id} endpoint deletes a user."""
    response = test_client.delete(f"/users/{user_id}")
    if response.status_code == 404:
        assert response.json()["detail"] == "User not found"
    else:
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"

