from uuid import UUID

class UserNotFound(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: UUID | None):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found.")

class UserInterestNotFound(Exception):
    """Exception raised when a user's interest is not found."""

    def __init__(self, interest: str):
        self.interest = interest
        super().__init__(f"Interest '{interest}' not found for the user.")

class UserAlreadyExists(Exception):
    """Exception raised when a user already exists."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists.")