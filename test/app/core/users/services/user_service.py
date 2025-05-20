from typing import List

from ..entities.user import CreateUserDto, User, UserInterests, UserRegistry
from ..protocols.user_repository import UserRepository
from .exceptions import UserAlreadyExists, UserNotFound


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
    user: UserRegistry,
    interest: UserInterests,
) -> User:
    """Add an interest to a user.

    Args:
        user_repository (UserRepository): The user repository instance.
        user (UserRegistry): The user to whom the interest will be added.
        interest (UserInterests): The interest to add.

    Raises:
        UserNotFound: If the user with the given ID does not exist.
        UserInterestAlreadyExists: If the interest already exists for the user.
    """
    ...  # TODO: Implement the logic to add an interest to a user


async def remove_interest(
    user_repository: UserRepository,
    user: UserRegistry,
    interest: UserInterests,
) -> User:
    """Remove an interest from a user.

    Args:
        user_repository (UserRepository): The user repository instance.
        user (UserRegistry): The user from whom the interest will be removed.
        interest (UserInterests): The interest to remove.

    Raises:
        UserNotFound: If the user with the given ID does not exist.
        UserInterestNotFound: If the interest does not exist for the user.
    """
    ...  # TODO: Implement the logic to remove an interest from a user


async def get_user_interests(
    user_repository: UserRepository,
    user: UserRegistry,
) -> List[UserInterests]:
    """Get all interests of a user.

    Args:
        user_repository (UserRepository): The user repository instance.
        user (UserRegistry): The user whose interests are to be fetched.

    Raises:
        UserNotFound: If the user with the given ID does not exist.
    """
    ...  # TODO: Implement the logic to get all interests of a user
