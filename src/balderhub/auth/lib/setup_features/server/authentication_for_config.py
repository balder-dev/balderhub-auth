from __future__ import annotations
import logging

from ... import scenario_features
from ...utils.resource_rule_list import ResourceRuleList

logger = logging.getLogger(__name__)


class AuthenticationForConfig(scenario_features.server.AuthenticationForConfig):
    """
    Basic Setup implementation of :class:`balderhub.auth.lib.scenario_features.server.AuthenticationForConfig`. It
    provides an implementation of :meth:`AuthenticationForConfig.get_resource_rules_that_require_no_authentication`,
    by subtracting the rule set of the rules that require auth from the existing rules.
    """

    existence_for = scenario_features.server.ExistenceForConfig()

    def get_resource_rules_that_require_authentication(self) -> ResourceRuleList:
        raise NotImplementedError

    def get_resource_rules_that_require_no_authentication(self) -> ResourceRuleList:
        return self.existence_for.get_resource_rules_that_exist() \
            - self.get_resource_rules_that_require_authentication()
