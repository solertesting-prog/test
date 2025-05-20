from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import SecretStr

from app.core.users.entities.user import UserRegistry
from app.core.users.services import user_service

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
    user = await user_service.get_user_by_username(
        user_repository=user_repository,
        username=form_data.username,
    )

    if not verify_password(SecretStr(form_data.password), user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return Token(
        access_token=create_access_token(user_registry=UserRegistry(id=user.id)),
        token_type="bearer",
    )
