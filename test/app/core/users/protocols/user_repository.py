from typing import Protocol, Optional
from uuid import UUID


from ..entities.user import User, CreateUserDto


class UserRepository(Protocol):
    """Protocol for user repository.
    
    This protocol defines the methods that a user repository should implement.
    """
    async def create(self, dto: CreateUserDto) -> User:
        """Create a new user in the database.
        Args:
            dto (CreateUserDto): The data transfer object containing user details.
        """
        ...

    async def fetch_by_id(self, id: UUID) -> Optional[User]:
        """fetch an active user by ID from the database.

        Args:
            id (UUID): The ID of the user to retrieve.
        """
        ...
    
    async def fetch_by_username(self, username: str) -> Optional[User]:
        """Fetch an active user by username from the database.

        Args:
            username (str): The username of the user to retrieve.
        """
        ...

    async def remove(self, id: UUID) -> User:
        """Make the user inactive in the database.

        Args:
            id (UUID): The ID of the user to remove.
        """
        ...
