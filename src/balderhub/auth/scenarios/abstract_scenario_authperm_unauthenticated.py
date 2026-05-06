from __future__ import annotations
import logging
import balder
from ..lib import scenario_features
from ..lib.utils.base_resource import BaseResource
from ..lib.utils.operation import Operation
from ..lib.utils.resource_rule import ResourceRule

logger = logging.getLogger(__name__)


class AbstractScenarioAuthpermUnauthenticated(balder.Scenario):
    """
    This is an abstract scenario for testing authentication and permissions when the user is not
    authenticated.

    .. image:: /_static/AbstractScenarioAuthpermUnauthenticated.svg
        :align: center
        :alt: Visual Description of this ``AbstractScenarioAuthpermUnauthenticated``
    """

    #: the expected exception(s) that should be raised when entering a non-existing resource/operation
    expected_operation_enter_exc_for_non_existing = [BaseResource.DoesNotExistError, Operation.DoesNotExistError]
    #: the expected exception(s) that should be raised when entering a resource/operation that requires authentication
    #: (but the client is not authenticated)
    expected_operation_enter_exc_for_no_auth = [BaseResource.UnauthorizedError, Operation.UnauthorizedError]

    class Server(balder.Device):
        """the server device that provides the resources"""
        #: feature for existence configuration
        existence = scenario_features.server.ExistenceForConfig()
        #: feature for authentication configuration
        needs_auth_for = scenario_features.server.AuthenticationForConfig()

    @balder.connect(Server, balder.Connection())  # pylint: disable=undefined-variable
    class UnauthClient(balder.Device):
        """the client device that is unauthenticated"""
        #: feature for unauthenticated check
        is_unauth = scenario_features.client.IsUnauthenticatedFeature()
        #: feature for operation handling
        operation = scenario_features.client.OperationHandlingFeature()

    def test_non_existing_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a non-existing resource raises the expected exception.

        :param resource_rule: the resource rule to test
        """
        raise NotImplementedError

    def test_no_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a resource that requires no authentication is possible.

        :param resource_rule: the resource rule to test
        """
        raise NotImplementedError

    def test_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a resource that requires authentication raises the expected exception.

        :param resource_rule: the resource rule to test
        """
        raise NotImplementedError
