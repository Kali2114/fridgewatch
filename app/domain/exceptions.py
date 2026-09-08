class DomainError(Exception):
    """Base class for domain-layer errors."""


class ItemNotFound(DomainError):
    """Raised when a repository lookup finds no item for the given id."""


class UserNotFound(DomainError):
    """Raised when a repository lookup finds no user for the given id."""


class EmailAlreadyRegistered(DomainError):
    """Raised when a user's email is already registered."""
