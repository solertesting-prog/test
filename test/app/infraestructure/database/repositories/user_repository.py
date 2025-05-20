from app.core.users.entities.user import CreateUserDto, User, UserInterests
from ..models.users import User as UserModel
from uuid import UUID
from typing import Optional



async def create(dto: CreateUserDto) -> User:
    """Create a new user in the database.

    Args:
        dto (CreateUserDto): The data transfer object containing user details.
    """
    user = await UserModel(**dto.model_dump()).insert()
    return User(**user.model_dump())

async def fetch_by_id(id: UUID) -> Optional[User]:
    """Fetch an active user by ID from the database.

    Args:
        id (UUID): The ID of the user to retrieve.
    """
    user = await UserModel.get(id)
    if not user:
        return None

    return User(**user.model_dump())


async def fetch_by_username(username: str) -> Optional[User]:
    """Fetch an active user by username from the database.

    Args:
        username (str): The username of the user to retrieve.
    """
    user = await UserModel.find_one(UserModel.username == username, UserModel.is_active == True)
    if not user:
        return None

    return User(**user.model_dump())

async def remove(id: UUID) -> User:
    raise NotImplementedError("User removal is not implemented yet.")