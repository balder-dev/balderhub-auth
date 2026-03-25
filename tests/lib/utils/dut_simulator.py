from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from balderhub.auth.lib.utils.action import Action
from balderhub.auth.lib.utils.operation import Operation
from balderhub.auth.lib.utils.resource import Resource


class DUTSimulator:
    """A simulator for a device-under-test (DUT) that manages resources with different access levels.

    Resources can be:
    - **public**: accessible without authentication
    - **authenticated**: require the user to be authenticated
    - **permission-based**: require the authenticated user to have specific permissions
    """

    def __init__(self):
        # all public available resources
        self._public_resources: Dict[Resource, List[Action]] = {}

        # all resources that need auth (permissions can only be granted to these type of resources)
        self._authenticated_resources: Dict[Resource, List[Action]] = {}

        self._authenticated_username: Optional[str] = None
        self._user_permissions: Dict[str, Set[Tuple[Resource, Action]]] = {}

    # -- authentication ------------------------------------------------------------------------------------------------

    def authenticate(self, username: str):
        """Authenticate as the given user."""
        self._authenticated_username = username

    def unauthenticate(self):
        """Clear the current authentication."""
        self._authenticated_username = None

    @property
    def authenticated_username(self) -> Optional[str]:
        """Returns the currently authenticated username or None."""
        return self._authenticated_username

    # -- user permissions ----------------------------------------------------------------------------------------------

    def grant_permission(self, username: str, resource: Resource, action: Action):
        """Grant a user permission to perform an action on a resource.

        :param username: the username to grant the permission to
        :param resource: the resource the permission applies to
        :param action: the action the permission applies to
        """
        self._user_permissions.setdefault(username, set()).add((resource, action))

    def revoke_permission(self, username: str, resource: Resource, action: Action):
        """Revoke a user's permission for an action on a resource.

        :param username: the username to revoke the permission from
        :param resource: the resource the permission applies to
        :param action: the action the permission applies to
        """
        if username in self._user_permissions:
            self._user_permissions[username].discard((resource, action))

    # -- resource registration -----------------------------------------------------------------------------------------

    def add_public_resource(self, resource: Resource, actions: Optional[List[Action]] = None):
        """Register a resource that is accessible without authentication.

        :param resource: the resource to add
        :param actions: optional list of actions available for this resource
        """
        self._public_resources[resource] = list(actions) if actions is not None else []

    def add_authenticated_resource(self, resource: Resource, actions: Optional[List[Action]] = None):
        """Register a resource that requires authentication.

        :param resource: the resource to add
        :param actions: optional list of actions available for this resource
        """
        self._authenticated_resources[resource] = list(actions) if actions is not None else []

    # -- operation execution -------------------------------------------------------------------------------------------

    def execute_operation(self, operation: Operation):
        """Execute an operation on the simulator.

        Checks are performed in the following order:
        1. Does the resource/action exist?
        2. If the resource requires authentication, is the user authenticated?
        3. If the resource/action requires permissions, does the user have them?

        :param operation: the operation to execute
        :raises Operation.DoesNotExistError: if the resource or action does not exist
        :raises Operation.UnauthorizedError: if authentication is required but the user is not authenticated
        :raises Operation.NoPermissionError: if the user lacks the required permission
        """
        resource = operation.resource
        action = operation.action

        # check if resources / actions exist
        if resource not in self.resources.keys():
            raise Operation.DoesNotExistError(f'resource `{resource}` does not exist in simulator')
        if action not in self.resources[resource]:
            raise Operation.DoesNotExistError(f'action `{action}` of resource `{resource}` does not exist in simulator')

        # check public resources
        if resource in self._public_resources:
            if action in self._public_resources[resource]:
                # resource is public
                return True

        # check authenticated resources
        if resource in self._authenticated_resources:
            assert action in self._authenticated_resources[resource], f'can not find action in auth-resources, but it is expected'

            if self.authenticated_username is None:
                raise Operation.UnauthorizedError( f'resource `{resource}` with action `{action}` requires authentication')

            user_perms = self._user_permissions.get(self._authenticated_username, set())
            if (resource, action) not in user_perms:
                raise Operation.NoPermissionError(
                    f'user `{self._authenticated_username}` lacks permission for `{action}` on `{resource}`')
            return True

        assert False, f"code should never be reached"

    # -- introspection -------------------------------------------------------------------------------------------------

    @property
    def resources(self) -> Dict[Resource, List[Action]]:
        """Returns a combined copy of all registered resources and their actions."""
        result = {}
        for resource, actions in self._public_resources.items():
            result[resource] = list(actions)
        for resource, actions in self._authenticated_resources.items():
            result[resource] = list(actions)
        return result
