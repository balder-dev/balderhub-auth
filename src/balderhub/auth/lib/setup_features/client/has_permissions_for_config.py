from __future__ import annotations

import logging
import balder

from ... import scenario_features
from ...utils.resource_rule_list import ResourceRuleList

logger = logging.getLogger(__name__)


class HasPermissionsForConfig(scenario_features.client.HasPermissionsForConfig):
    """
    Basic Setup implementation of :class:`balderhub.auth.lib.scenario_features.client.HasPermissionsForConfig`. It
    provides an implementation of :meth:`HasPermissionsForConfig.get_resource_rules_without_permissions`,
    by subtracting the rule set of the rules that require permissions from the rules that require authentication.
    """

    class Server(balder.VDevice):
        """VDevice representing the server."""
        auth_for = scenario_features.server.AuthenticationForConfig()

    def get_resource_rules_with_permissions(self) -> ResourceRuleList:
        raise NotImplementedError()

    def get_resource_rules_without_permissions(self) -> ResourceRuleList:
        return self.Server.auth_for.get_resource_rules_that_require_authentication() \
            - self.get_resource_rules_with_permissions()
