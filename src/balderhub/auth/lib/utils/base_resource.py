from abc import ABC
from typing import TypeVar


class BaseResource(ABC):
    """
    This is the base class for all resource types.
    """

    class ResourceEnterError(Exception):
        """
        Base exception for all errors that occur when entering a resource.
        """

    class DoesNotExistError(ResourceEnterError):
        """
        Exception that is raised if a resource does not exist.
        """

    class UnauthorizedError(ResourceEnterError):
        """
        Exception that is raised if the user is not authorized to access a resource.
        """

    class NoPermissionError(ResourceEnterError):
        """
        Exception that is raised if the user has no permission to access a resource.
        """

    def __str__(self):
        return f"{self.__class__.__name__}"


BaseResourceT = TypeVar('BaseResourceT', bound=BaseResource)
