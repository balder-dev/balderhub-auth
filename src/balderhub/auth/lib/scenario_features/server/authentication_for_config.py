from __future__ import annotations
import logging
import balder

from ...utils.resource_rule_list import ResourceRuleList

logger = logging.getLogger(__name__)


class AuthenticationForConfig(balder.Feature):
    """
    This feature class represents the authentication rule configuration for a server device.
    """

    @property
    def resolved_resources_that_require_authentication(self):
        """returns the list of resolved resource rules, that require authentication"""
        return self.get_resource_rules_that_require_authentication().filter_for_resolved_only()

    @property
    def resolved_resources_that_require_no_authentication(self):
        """returns the list of resolved resource rules, that require NO authentication"""
        return self.get_resource_rules_that_require_no_authentication().filter_for_resolved_only()

    @property
    def unresolved_resources_that_require_authentication(self):
        """returns the list of unresolved resource rules, that require authentication"""
        return self.get_resource_rules_that_require_authentication().filter_for_unresolved_only()

    @property
    def unresolved_resources_that_require_no_authentication(self):
        """returns the list of unresolved resource rules, that require NO authentication"""
        return self.get_resource_rules_that_require_no_authentication().filter_for_unresolved_only()

    def get_resource_rules_that_require_authentication(self) -> ResourceRuleList:
        """
        Returns the list of resource rules, that require authentication.

        :return: the resource rule list
        """
        raise NotImplementedError

    def get_resource_rules_that_require_no_authentication(self) -> ResourceRuleList:
        """
        Returns the list of resource rules, that require NO authentication.

        :return: the resource rule list
        """
        # TODO this method can be auto calculated!!
        raise NotImplementedError
