from typing import List, Optional
from uuid import UUID

from ..entities.user import CreateUserDto, User, UserInterests, UserRegistry
from ..protocols.user_repository import UserRepository
from .exceptions import UserAlreadyExists, UserInterestAlreadyExists, UserInterestNotFound, UserNotFound


async def create_user(
    user_repository: UserRepository,
    dto: CreateUserDto,
) -> User:
    """Create a new user in the database.

    Args:
        user_repository (UserRepository): The user repository instance.
        dto (CreateUserDto): The data transfer object containing user details.
    """
    created_user = await user_repository.create(dto)
    # We assume that the repository implementation will return None if
    # the user already exists
    if not created_user:
        raise UserAlreadyExists(dto.email)

    return created_user

async def delete_user(
    user_repository: UserRepository,
    userId: UUID,
) -> User:
    fetched_user = await user_repository.fetch_by_id(userId)
    if not fetched_user:
        raise UserNotFound(userId)

    deleted_user = await user_repository.remove(userId)

    return deleted_user

async def get_user_by_username(
    user_repository: UserRepository,
    username: str,
) -> User:
    """Get a user by their username.

    Args:
        user_repository (UserRepository): The user repository instance.
        username (str): The username of the user to retrieve.

    Raises:
        UserNotFound: If the user with the given username does not exist.
    """
    fetched_user = await user_repository.fetch_by_username(username)
    if not fetched_user:
        raise UserNotFound(None)
    return fetched_user


async def get_user_by_id(
    user_repository: UserRepository,
    user: UserRegistry,
) -> User:
    """Get a user by their ID.

    Args:
        user_repository (UserRepository): The user repository instance.
        user (UserRegistry): The user whose details are to be fetched.

    Raises:
        UserNotFound: If the user with the given ID does not exist.
    """
    fetched_user = await user_repository.fetch_by_id(user.id)
    if not fetched_user:
        raise UserNotFound(user.id)

    return fetched_user


async def add_interest(
    user_repository: UserRepository,
    userID: UUID,
    interest: UserInterests,
) -> Optional[User]:
    """Add an interest to a user.

    Args:
        user_repository (UserRepository): The user repository instance.
        userID (UUID): The ID of the user to whom the interest will be added.
        interest (UserInterests): The interest to add.

    Raises:
        UserNotFound: If the user with the given ID does not exist.
        UserInterestAlreadyExists: If the interest already exists for the user.

    Returns:
        User: The updated user after adding the interest.
    """
    user = await user_repository.fetch_by_id(userID)
    if not user:
        raise UserNotFound(userID)

    if interest in user.interests:
        raise UserInterestAlreadyExists(interest)

    updated_user = await user_repository.add_user_interest(userID, interest)

    logging.info(f"Interest '{interest}' added to user with ID {userID}")

    return updated_user


import logging

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del mensaje
)


async def remove_interest(
    user_repository: UserRepository,
    userID: UUID,
    interest: UserInterests,
) -> Optional[User]:
    """Remove an interest from a user.

    Args:
        user_repository (UserRepository): The user repository instance.
        userID (UUID): The ID of the user from whom the interest will be removed.
        interest (UserInterests): The interest to remove.

    Raises:
        UserNotFound: If the user with the given ID does not exist.
        UserInterestNotFound: If the interest does not exist for the user.

    Returns:
        User: The updated user after removing the interest.
    """
    user = await user_repository.fetch_by_id(userID)
    if not user:
        raise UserNotFound(userID)

    if interest not in user.interests:
        raise UserInterestNotFound(interest)

    updated_user = await user_repository.remove_user_interest(userID, interest)

 
    return updated_user

async def get_user_interests(
    user_repository: UserRepository,
    userId: UUID,
) -> List[UserInterests]:
    user_interests = await user_repository.fetch_user_interests(userId)
    if not user_interests:
        raise UserNotFound(userId)

    return user_interests


