from typing import TypeVar

from .action import Action
from .resource import Resource


class Operation:
    """
    This class represents an operation, which is a combination of a resource and an action.
    """

    class OperationEnterError(Exception):
        """
        Base exception for all errors that occur when executing an operation.
        """

    class DoesNotExistError(OperationEnterError):
        """
        Exception that is raised if the peration does not exist.
        """

    class UnauthorizedError(OperationEnterError):
        """
        Exception that is raised if the user is not authorized to perform the action on the resource.
        """

    class NoPermissionError(OperationEnterError):
        """
        Exception that is raised if the user has no permission to perform the action on the resource.
        """

    def __init__(self, resource: Resource, action: Action):
        """
        :param resource: the resource of the operation
        :param action: the action of the operation
        """

        if not isinstance(resource, Resource):
            raise TypeError(f'resource must be of type {Resource.__name__}')
        if not isinstance(action, Action):
            raise TypeError(f'action must be of type {Action.__name__}')

        self._resource = resource
        self._action = action

    def __str__(self):
        return f'{self.__class__.__name__}<{self.resource}:{[str(self.action)]}>'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.resource == other.resource and self.action == other.action

    @property
    def resource(self) -> Resource:
        """returns the resource of this operation"""
        return self._resource

    @property
    def action(self) -> Action:
        """returns the action of this operation"""
        return self._action


OperationT = TypeVar('OperationT', bound=Operation)
