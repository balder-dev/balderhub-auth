from __future__ import annotations
import logging
import balder

from ..lib import scenario_features
from ..lib.utils.resource_rule import ResourceRule
from .abstract_scenario_authperm_authenticated import AbstractScenarioAuthpermAuthenticated


logger = logging.getLogger(__name__)


class ScenarioAuthpermAuthenticatedObjperm(AbstractScenarioAuthpermAuthenticated):
    """
    This scenario tests authentication and permission handling for an authenticated client with object-level
    permissions by resolving unresolved resources with parameters and verifying the behavior of non-existing
    resources, resources that require no authentication, resources the client has no permission for, and resources
    the client has permission for.
    """

    class Server(AbstractScenarioAuthpermAuthenticated.Server):
        """the server device that provides the resources"""
        existence = scenario_features.server.ExistenceForConfig()
        needs_auth_for = scenario_features.server.AuthenticationForConfig()

    @balder.connect('Server', balder.Connection())
    class Client(AbstractScenarioAuthpermAuthenticated.Client):
        """the authenticated client device that accesses the resources with object-level permissions"""
        param_provider = scenario_features.client.UnresolvedResourceParameterConfig()
        sm_auth = scenario_features.client.AuthenticationStateMachine()
        operation = scenario_features.client.OperationHandlingFeature()
        has_perm_for = scenario_features.client.HasPermissionsForConfig()

    @balder.fixture('testcase')
    def make_sure_to_be_authenticated(self):
        """
        Makes sure that the client is authenticated before the testcase starts.
        """
        # TODO BALDER BUG: self.Client.sm_auth will not be set correctly in subclass!!!!!!!
        if self.Client.sm_auth.current_state != self.Client.sm_auth.State.AUTHENTICATED:
            logger.info('client is not authenticated yet - authenticate it')
            self.Client.sm_auth.change_state_to(self.Client.sm_auth.State.AUTHENTICATED)
        else:
            logger.info('client is already authenticated')

    @balder.parametrize_by_feature(
        'resource_rule', (Server, 'existence', 'unresolved_resources_that_not_exist')
    )
    def test_non_existing_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing a non-existing unresolved resource raises the expected exception or returns False.
        Resolves the resource rule with each parameter and verifies the behavior for each resulting operation.

        :param resource_rule: the resource rule for a non-existing unresolved resource
        """
        self.Client.sm_auth.assert_expected_state(self.Client.sm_auth.State.AUTHENTICATED)

        for cur_param in self.Client.param_provider.get_parameters_for(resource_rule):
            operations = resource_rule.resolve(cur_param)

            if operations is None:
                # parameter does not match rule - skip
                continue

            for cur_operation in operations:
                self.Client.operation.prepare_operation(cur_operation)
                try:
                    logger.info(f"enter operation {cur_operation}")
                    assert not self.Client.operation.enter_operation(cur_operation), \
                        (f'operation was entered successfully, but should raise one of the following exceptions: '
                         f'`{self.expected_operation_enter_exc_for_non_existing}` or return False')
                except tuple(self.expected_operation_enter_exc_for_non_existing) as exc:
                    logger.debug(f'entering of operation that does not exist raises expected `{exc}`')
                finally:
                    self.Client.operation.cleanup_operation(cur_operation)

    @balder.parametrize_by_feature(
        'resource_rule', (Server, 'needs_auth_for', 'unresolved_resources_that_require_no_authentication')
    )
    def test_no_auth_requiring_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing an unresolved resource that requires no authentication can be entered and left
        successfully. Resolves the resource rule with each parameter and verifies the behavior for each resulting
        operation.

        :param resource_rule: the resource rule for an unresolved resource that requires no authentication
        """
        self.Client.sm_auth.assert_expected_state(self.Client.sm_auth.State.AUTHENTICATED)

        for cur_param in self.Client.param_provider.get_parameters_for(resource_rule):
            operations = resource_rule.resolve(cur_param)

            if operations is None:
                # parameter does not match rule - skip
                continue

            for cur_operation in operations:

                self.Client.operation.prepare_operation(cur_operation)
                try:
                    logger.info(f"enter operation {cur_operation}")
                    assert self.Client.operation.enter_operation(cur_operation), \
                        f"entering operation {cur_operation} returns False"
                    logger.debug('operation was entered successfully')
                    logger.info(f"leave operation {cur_operation}")
                    assert self.Client.operation.leave_operation(cur_operation), \
                        f"leaving operation {cur_operation} returns False"
                    logger.debug('operation was leaved successfully')
                finally:
                    self.Client.operation.cleanup_operation(cur_operation)

    @balder.parametrize_by_feature(
        'resource_rule', (Client, 'has_perm_for', 'unresolved_resources_without_permissions')
    )
    def test_client_has_no_perm_for_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing an unresolved resource the client has no permission for raises the expected exception
        or returns False. Resolves the resource rule with each parameter and verifies the behavior for each
        resulting operation.

        :param resource_rule: the resource rule for an unresolved resource the client has no permission for
        """
        self.Client.sm_auth.assert_expected_state(self.Client.sm_auth.State.AUTHENTICATED)

        for cur_param in self.Client.param_provider.get_parameters_for(resource_rule):
            operations = resource_rule.resolve(cur_param)

            if operations is None:
                # parameter does not match rule - skip
                continue

            for cur_operation in operations:
                self.Client.operation.prepare_operation(cur_operation)
                try:
                    logger.info(f"enter operation {cur_operation}")
                    assert not self.Client.operation.enter_operation(cur_operation), \
                        (f'operation was entered successfully, but should raise one of the following exceptions: '
                         f'`{self.expected_operation_enter_exc_for_no_perm}` or return False')
                except tuple(self.expected_operation_enter_exc_for_no_perm) as exc:
                    logger.debug(f'entering of operation with client that has no permission for it raises '
                                 f'expected `{exc}`')
                finally:
                    self.Client.operation.cleanup_operation(cur_operation)

    @balder.parametrize_by_feature(
        'resource_rule', (Client, 'has_perm_for', 'unresolved_resources_with_permissions')
    )
    def test_client_has_perm_for_resources(self, resource_rule: ResourceRule):
        """
        Tests that accessing an unresolved resource the client has permission for can be entered and left
        successfully. Resolves the resource rule with each parameter and verifies the behavior for each resulting
        operation.

        :param resource_rule: the resource rule for an unresolved resource the client has permission for
        """
        self.Client.sm_auth.assert_expected_state(self.Client.sm_auth.State.AUTHENTICATED)

        for cur_param in self.Client.param_provider.get_parameters_for(resource_rule):
            operations = resource_rule.resolve(cur_param)

            if operations is None:
                # parameter does not match rule - skip
                continue

            for cur_operation in operations:
                self.Client.operation.prepare_operation(cur_operation)
                try:
                    logger.info(f"enter operation {cur_operation}")
                    assert self.Client.operation.enter_operation(cur_operation), \
                        f"entering operation {cur_operation} returns False"
                    logger.debug('operation was entered successfully')
                    logger.info(f"leave operation {cur_operation}")
                    assert self.Client.operation.leave_operation(cur_operation), \
                        f"leaving operation {cur_operation} returns False"
                    logger.debug('operation was leaved successfully')
                finally:
                    self.Client.operation.cleanup_operation(cur_operation)
