from __future__ import annotations
import logging
import balder

from ..lib import scenario_features
from ..lib.utils.resource_rule import ResourceRule
from .abstract_scenario_authperm_unauthenticated import AbstractScenarioAuthpermUnauthenticated

logger = logging.getLogger(__name__)


class ScenarioAuthpermUnauthenticatedObjperm(AbstractScenarioAuthpermUnauthenticated):
    """
    This scenario tests the authentication and permission handling for unauthenticated access with object-level
    permissions. It resolves unresolved resources using parameters provided by the client and validates that the
    system correctly handles non-existing resources, resources that do not require authentication, and resources
    that require authentication.
    """

    class Server(AbstractScenarioAuthpermUnauthenticated.Server):
        """The server device that provides existence and authentication configuration features."""
        existence = scenario_features.server.ExistenceForConfig()
        needs_auth_for = scenario_features.server.AuthenticationForConfig()

    @balder.connect('Server', balder.Connection())
    class UnauthClient(AbstractScenarioAuthpermUnauthenticated.UnauthClient):
        """The unauthenticated client device that provides parameter resolution and operation handling features."""
        param_provider = scenario_features.client.UnresolvedResourceParameterConfig()
        is_unauth = scenario_features.client.IsUnauthenticatedFeature()
        operation = scenario_features.client.OperationHandlingFeature()

    @balder.parametrize_by_feature('resource_rule', (Server, 'existence', 'unresolved_resources_that_not_exist'))
    def test_non_existing_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing non-existing resources with an unauthenticated client fails as expected. Resolves
        each resource rule with available parameters and verifies that entering the operation either returns False
        or raises one of the expected exceptions.
        """
        for cur_param in self.UnauthClient.param_provider.get_parameters_for(resource_rule):
            operations = resource_rule.resolve(cur_param)

            if operations is None:
                # parameter does not match rule - skip
                continue

            for cur_operation in operations:
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
        'resource_rule', (Server, 'needs_auth_for', 'unresolved_resources_that_require_no_authentication')
    )
    def test_no_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that resources which do not require authentication can be successfully accessed by an unauthenticated
        client. Resolves each resource rule with available parameters and verifies that the operation can be
        entered and left successfully.
        """
        # todo use `(all_data - own_data)`
        #  -> client should not have access because its the data that is only available for clients that are auth
        for cur_param in self.UnauthClient.param_provider.get_parameters_for(resource_rule):
            operations = resource_rule.resolve(cur_param)

            if operations is None:
                # parameter does not match rule - skip
                continue

            for cur_operation in operations:

                self.UnauthClient.operation.prepare_operation(cur_operation)
                try:
                    logger.info(f"enter operation {cur_operation}")
                    assert self.UnauthClient.operation.enter_operation(cur_operation), \
                        f"entering operation {cur_operation} returns False"
                    logger.debug('operation was entered successfully')
                    logger.info(f"leave operation {cur_operation}")
                    assert self.UnauthClient.operation.leave_operation(cur_operation), \
                        f"leaving operation {cur_operation} returns False"
                    logger.debug('operation was leaved successfully')
                finally:
                    self.UnauthClient.operation.cleanup_operation(cur_operation)

    @balder.parametrize_by_feature(
        'resource_rule', (Server, 'needs_auth_for', 'unresolved_resources_that_require_authentication')
    )
    def test_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that resources which require authentication cannot be accessed by an unauthenticated client. Resolves
        each resource rule with available parameters and verifies that entering the operation either returns False
        or raises one of the expected exceptions.
        """
        for cur_param in self.UnauthClient.param_provider.get_parameters_for(resource_rule):
            operations = resource_rule.resolve(cur_param)

            if operations is None:
                # parameter does not match rule - skip
                continue

            for cur_operation in operations:
                self.UnauthClient.operation.prepare_operation(cur_operation)
                try:
                    logger.info(f"enter operation {cur_operation}")
                    assert not self.UnauthClient.operation.enter_operation(cur_operation), \
                        (f'operation was entered successfully, but should raise one of the following exceptions: '
                         f'`{self.expected_operation_enter_exc_for_no_auth}` or return False')
                except tuple(self.expected_operation_enter_exc_for_no_auth) as exc:
                    logger.debug(f'entering of operation with client that has no permission for it raises '
                                 f'expected `{exc}`')
                finally:
                    self.UnauthClient.operation.cleanup_operation(cur_operation)
