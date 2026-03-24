from __future__ import annotations
import logging
import balder

from .abstract_scenario_authperm_unauthenticated import AbstractScenarioAuthpermUnauthenticated
from ..lib import scenario_features
from ..lib.utils.resource_rule import ResourceRule

logger = logging.getLogger(__name__)


class ScenarioAuthpermUnauthenticated(AbstractScenarioAuthpermUnauthenticated):
    """
    This scenario tests authentication and permission handling for an unauthenticated client by verifying the behavior
    of non-existing resources, resources that require no authentication, and resources that require authentication.
    """

    class Server(AbstractScenarioAuthpermUnauthenticated.Server):
        """the server device that provides the resources"""
        existence = scenario_features.server.ExistenceForConfig()
        needs_auth_for = scenario_features.server.AuthenticationForConfig()

    @balder.connect('Server', balder.Connection())
    class UnauthClient(AbstractScenarioAuthpermUnauthenticated.UnauthClient):
        """the unauthenticated client device that accesses the resources"""
        is_unauth = scenario_features.client.IsUnauthenticatedFeature()
        operation = scenario_features.client.OperationHandlingFeature()

    @balder.parametrize_by_feature(
        'resource_rule', (Server, 'existence', 'resolved_resources_that_not_exist')
    )
    def test_non_existing_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a non-existing resource raises the expected exception or returns False.

        :param resource_rule: the resource rule for a non-existing resource
        """
        for cur_operation in resource_rule.resolve():
            self.UnauthClient.operation.prepare_operation(cur_operation)
            try:
                logger.info(f"enter operation {cur_operation}")
                assert not self.UnauthClient.operation.enter_operation(cur_operation), \
                    (f'operation was entered successfully, but should raise one of the following exceptions: '
                     f'`{self.expected_operation_enter_exc_for_non_existing}` or return False')
            except tuple(self.expected_operation_enter_exc_for_non_existing) as exc:
                logger.debug(f'entering of operation that does not exist raises expected `{exc}`')
            finally:
                self.UnauthClient.operation.cleanup_operation(cur_operation)

    @balder.parametrize_by_feature(
        'resource_rule', (Server, 'needs_auth_for', 'resolved_resources_that_require_no_authentication')
    )
    def test_no_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a resource that requires no authentication can be entered and left successfully.

        :param resource_rule: the resource rule for a resource that requires no authentication
        """
        for cur_operation in resource_rule.resolve():
            self.UnauthClient.operation.prepare_operation(cur_operation)
            try:
                logger.info(f"enter operation {cur_operation}")
                assert self.UnauthClient.operation.enter_operation(cur_operation), "entering of operation returns False"
                logger.debug('operation was entered successfully')
                logger.info(f"leave operation {cur_operation}")
                assert self.UnauthClient.operation.leave_operation(cur_operation), "leaving operation returns False"
                logger.debug('operation was leaved successfully')
            finally:
                self.UnauthClient.operation.cleanup_operation(cur_operation)

    @balder.parametrize_by_feature(
        'resource_rule', (Server, 'needs_auth_for', 'resolved_resources_that_require_authentication')
    )
    def test_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a resource that requires authentication raises the expected exception or returns False.

        :param resource_rule: the resource rule for a resource that requires authentication
        """
        for cur_operation in resource_rule.resolve():
            self.UnauthClient.operation.prepare_operation(cur_operation)
            try:
                logger.info(f"enter operation {cur_operation}")
                assert not self.UnauthClient.operation.enter_operation(cur_operation), \
                    (f'operation was entered successfully, but should raise one of the following exceptions: '
                     f'`{self.expected_operation_enter_exc_for_no_auth}` or return False')
            except tuple(self.expected_operation_enter_exc_for_no_auth) as exc:
                logger.debug(f'entering of operation with client that has no permission for it raises expected `{exc}`')
            finally:
                self.UnauthClient.operation.cleanup_operation(cur_operation)
