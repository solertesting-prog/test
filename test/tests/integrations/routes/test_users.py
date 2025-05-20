from fastapi.testclient import TestClient

from app.infraestructure.database.seed import (
    TEST_EMAIL,
    TEST_INTERESTS,
    TEST_PASSWORD,
    TEST_USERNAME,
)


async def test_unregistered_user(test_client: TestClient) -> None:
    """Test that the /users/me endpoint returns a 401 for an unregistered user."""
    response = test_client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


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


async def test_get_user_info_unauthorized(test_client: TestClient) -> None:
    """Test that the /users/me endpoint returns a 401 for unauthorized access."""
    response = test_client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
