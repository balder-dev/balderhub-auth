import balder

from ...utils.resource_rule_list import ResourceRuleList


class ExistenceForConfig(balder.Feature):
    """
    This feature class represents the existence rule configuration for a server device.
    """

    @property
    def resolved_resources_that_exists(self):
        """returns the list of resolved resource rules, that exist"""
        return self.get_resource_rules_that_exist().filter_for_resolved_only()

    @property
    def resolved_resources_that_not_exist(self):
        """returns the list of resolved resource rules, that do NOT exist"""
        return self.get_resource_rules_that_not_exist().filter_for_resolved_only()

    @property
    def unresolved_resources_that_exists(self):
        """returns the list of unresolved resource rules, that exist"""
        return self.get_resource_rules_that_exist().filter_for_unresolved_only()

    @property
    def unresolved_resources_that_not_exist(self):
        """returns the list of unresolved resource rules, that do NOT exist"""
        return self.get_resource_rules_that_not_exist().filter_for_unresolved_only()

    def get_resource_rules_that_exist(self) -> ResourceRuleList:
        """
        Returns the list of resource rules, that exist.

        :return: the resource rule list
        """
        raise NotImplementedError

    def get_resource_rules_that_not_exist(self) -> ResourceRuleList:
        """
        Returns the list of resource rules, that do NOT exist.

        :return: the resource rule list
        """
        raise NotImplementedError
