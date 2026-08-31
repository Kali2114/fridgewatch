class DomainError(Exception):
    """Base class for domain-layer errors."""


class ItemNotFound(DomainError):
    """Raised when a repository lookup finds no item for the given id."""
