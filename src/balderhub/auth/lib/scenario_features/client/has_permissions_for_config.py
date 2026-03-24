from __future__ import annotations

import logging
import balder

from ...utils.resource_rule_list import ResourceRuleList

logger = logging.getLogger(__name__)


class HasPermissionsForConfig(balder.Feature):
    """
    This feature class represents the permission rule configuration for a user device.
    """

    @property
    def resolved_resources_with_permissions(self):
        """returns the list of resolved resource rules, the user has permissions"""
        return self.get_resource_rules_with_permissions().filter_for_resolved_only()

    @property
    def resolved_resources_without_permissions(self):
        """returns the list of resolved resource rules, the user has NO permissions"""
        return self.get_resource_rules_without_permissions().filter_for_resolved_only()

    @property
    def unresolved_resources_with_permissions(self):
        """returns the list of unresolved resource rules, the user has permissions"""
        return self.get_resource_rules_with_permissions().filter_for_unresolved_only()

    @property
    def unresolved_resources_without_permissions(self):
        """returns the list of unresolved resource rules, the user has NO permissions"""
        return self.get_resource_rules_without_permissions().filter_for_unresolved_only()

    def get_resource_rules_with_permissions(self) -> ResourceRuleList:
        """
        Returns the list of resource rules, the user has permissions.

        :return: the resource rule list
        """
        raise NotImplementedError()

    def get_resource_rules_without_permissions(self) -> ResourceRuleList:
        """
        Returns the list of resource rules, the user has NO permissions

        :return: the resource rule list
        """
        # TODO this method can be auto calculated!!
        raise NotImplementedError()
