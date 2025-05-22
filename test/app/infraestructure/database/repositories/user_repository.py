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

async def remove(id: UUID) -> Optional[User]:
    user = await UserModel.get(id)
    if not user:
        return None  

    await user.delete()

    return User(**user.model_dump())

import logging

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del mensaje
)

async def fetch_user_interests(user_id: UUID) -> Optional[list[UserInterests]]:
    logging.info(f"Fetching interests for user with ID: {user_id}")

    user = await UserModel.get(user_id)
    if not user:
        return None
    
    logging.info(f"Interests for user {user_id}: {user.interests}")

    return user.interests

async def remove_user_interest(user_id: UUID, interest: str) -> Optional[User]:
    """Remove a specific interest from a user in the database.

    Args:
        user_id (UUID): The ID of the user whose interest will be removed.
        interest (str): The interest to remove.

    Returns:
        Optional[User]: The updated user if the operation is successful, or None if the user does not exist.
    """
    logging.info(f"Removing interest '{interest}' for user with ID: {user_id}")

    user = await UserModel.get(user_id)
    if not user:
        logging.warning(f"User with ID {user_id} not found.")
        return None

    if interest not in user.interests:
        logging.warning(f"Interest '{interest}' not found for user with ID {user_id}.")
        return None

    user.interests.remove(interest)

    await user.save()

    logging.info(f"Interest '{interest}' removed for user with ID {user_id}.")
    return User(**user.model_dump())