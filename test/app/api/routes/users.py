from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from app.core.users.entities.user import UserRegistry
from app.core.users.services import user_service
from app.core.users.services.exceptions import UserNotFound

from ..auth import Token, create_access_token, verify_password
from ..container import dependencies, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

user_repository = dependencies().user_repository


@router.get("/me")
async def get_user_info(user: UserRegistry = Depends(get_current_user)):
    """Get the current user's information."""
    user_data = await user_service.get_user_by_id(
        user_repository=user_repository,
        user=user,
    )
    return user_data


@router.post("/auth")
async def auth_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Authenticate a user and return a JWT token."""

    try:
        user = await user_service.get_user_by_username(
            user_repository=user_repository,
            username=form_data.username,
        )
    except UserNotFound:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(SecretStr(form_data.password), user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return Token(
        access_token=create_access_token(user_registry=UserRegistry(id=user.id)),
        token_type="bearer",
    )

@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    try:
        deleted_user = await user_service.delete_user(
            user_repository=user_repository,
            userId=user_id,
        )
        return {"message": "User deleted successfully", "user": deleted_user}
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))