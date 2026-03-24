from __future__ import annotations
import logging
import balder
from ..lib import scenario_features
from ..lib.utils.base_resource import BaseResource
from ..lib.utils.operation import Operation
from ..lib.utils.resource_rule import ResourceRule

logger = logging.getLogger(__name__)


class AbstractScenarioAuthpermAuthenticated(balder.Scenario):
    """
    This is an abstract scenario for testing authentication and permissions when the user is already
    authenticated.
    """

    #: the expected exception(s) that should be raised when entering a non-existing resource/operation
    expected_operation_enter_exc_for_non_existing = [BaseResource.DoesNotExistError, Operation.DoesNotExistError]
    #: the expected exception(s) that should be raised when entering a resource/operation that requires authentication
    #: (but the client is already authenticated - this should only be raised if the resource is not existing or
    #: the user has no permissions)
    expected_operation_enter_exc_for_no_auth = [BaseResource.UnauthorizedError, Operation.UnauthorizedError]
    #: the expected exception(s) that should be raised when entering a resource/operation that the client has no
    #: permission for
    expected_operation_enter_exc_for_no_perm = [BaseResource.NoPermissionError, Operation.NoPermissionError]

    class Server(balder.Device):
        """the server device that provides the resources"""
        existence = scenario_features.server.ExistenceForConfig()
        needs_auth_for = scenario_features.server.AuthenticationForConfig()

    @balder.connect(Server, balder.Connection())  # pylint: disable=undefined-variable
    class Client(balder.Device):
        """the client device that accesses the resources"""
        sm_auth = scenario_features.client.AuthenticationStateMachine()
        operation = scenario_features.client.OperationHandlingFeature()
        has_perm_for = scenario_features.client.HasPermissionsForConfig()

    @balder.fixture('testcase')
    def make_sure_to_be_authenticated(self):
        """
        Makes sure that the client is authenticated before the testcase starts.
        """
        if self.Client.sm_auth.current_state != self.Client.sm_auth.State.AUTHENTICATED:
            logger.info('client is not authenticated yet - authenticate it')
            self.Client.sm_auth.change_state_to(self.Client.sm_auth.State.AUTHENTICATED)
        else:
            logger.info('client is already authenticated')

    def test_non_existing_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a non-existing resource raises the expected exception.

        :param resource_rule: the resource rule to test
        """
        raise NotImplementedError

    def test_no_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a resource that requires no authentication is possible even with an authentificated user.

        :param resource_rule: the resource rule to test
        """
        raise NotImplementedError

    def test_client_has_no_perm_for_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a resource the client has no permission for raises the expected exception.

        :param resource_rule: the resource rule to test
        """
        raise NotImplementedError

    def test_client_has_perm_for_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a resource the client has permission for is possible.

        :param resource_rule: the resource rule to test
        """
        raise NotImplementedError
