from __future__ import annotations

from typing import Iterable

from .unresolved_resource import UnresolvedResource
from .resource_rule import ResourceRule
from .resource import Resource
from .action import Action


class ResourceRuleList:
    """
    This class represents a list of resource rules.
    """

    # todo make sure that these checks are done everywhere!

    def __init__(self, iterable: Iterable[ResourceRule] = None):
        """
        :param iterable: an optional iterable of resource rules to initialize the list with
        """

        self._rules = []

        if iterable is not None:
            for rule in iterable:
                self.append(rule)

    def __iter__(self) -> Iterable[ResourceRule]:
        return self._rules.__iter__()

    def __len__(self):
        return self._rules.__len__()

    def __eq__(self, other):
        return self.rules == other.rules

    @property
    def rules(self) -> list[ResourceRule]:
        """returns the list of rules"""
        return self._rules.copy()

    def append(self, rule: ResourceRule):
        """
        Appends a resource rule to the list.

        :param rule: the resource rule to append
        """
        if not isinstance(rule, ResourceRule):
            raise TypeError(f'rule must be an instance of `{ResourceRule.__name__}`')
        if rule in self._rules:
            raise ValueError(f'object `{rule}` can not be added multiple times')
        self._rules.append(rule)

    def extend(self, other: ResourceRuleList):
        """
        Extends the list with the rules from another `ResourceRuleList`.

        :param other: the other `ResourceRuleList` to extend this list with
        """
        if not isinstance(other, ResourceRuleList):
            raise TypeError(f'object must be an instance of `{ResourceRuleList.__name__}`')
        for cur_obj in other:
            if cur_obj not in self._rules:
                self._rules.append(cur_obj)

    def flatten_and_group_by_resource_and_action(self) -> dict[Resource, dict[Action, ResourceRule]]:
        """
        Flattens the rules and groups them by resource and action.

        :return: a dictionary where the keys are resources and the values are dictionaries where the keys are
                 actions and the values are the corresponding resource rules
        """
        flatten_self = self.flatten()
        result = {}
        for cur_obj in flatten_self:
            if cur_obj.resource not in result.keys():
                result[cur_obj.resource] = {}

            if len(cur_obj.actions) != 1:
                raise ValueError(f'detect flatten resource with != one action: actions are `{cur_obj.actions}`')
            result[cur_obj.resource][cur_obj.actions[0]] = cur_obj
        return result

    def flatten(self) -> ResourceRuleList:
        """
        Goes through every list item and converts it to a list of ResourceRules with exactly one Action
        :return: a flatten ResourceRuleList, where every ResourceRule has exactly one Action
        """
        new_rules = []
        for rule in self._rules:
            new_rules.extend(rule.flatten())
        return ResourceRuleList(new_rules)

    def __sub__(self, other: ResourceRuleList) -> ResourceRuleList:
        """
        Subtracts the rules of another `ResourceRuleList` from this list.

        If a rule is in both lists, the rule of the resulting `ResourceRuleList` will be updated to
        `[self].rule and NOT [other].rule`.

        :param other: the other `ResourceRuleList` to subtract from this list
        :return: a new `ResourceRuleList` containing the result of the subtraction
        """
        # if it is in self, but not in other: add it to result unchanged
        # if it is in other, but not in self: raise an execption
        # if it is in both: add it to other, but change rule to `[self].rule and NOT [other].rule`

        if not isinstance(other, ResourceRuleList):
            raise TypeError(f'object must be an instance of `{ResourceRuleList.__name__}`')

        # sort by Resource and Action
        grouped_self = self.flatten_and_group_by_resource_and_action()
        grouped_other = other.flatten_and_group_by_resource_and_action()

        # check if one resource is in other but not in this one
        for cur_resource, resource_dict in grouped_other.items():
            for cur_action, cur_other_resource_rule in resource_dict.items():
                if grouped_self.get(cur_resource, {}).get(cur_action) is None:
                    raise ValueError(f'element `{cur_other_resource_rule}` from the list being subtracted is not '
                                     f'present in the current list')

        result = []
        for cur_resource, resource_dict in grouped_self.items():

            for cur_action, cur_self_resource_rule in resource_dict.items():
                other_resource_rule = grouped_other.get(cur_resource, {}).get(cur_action)
                if other_resource_rule is None:
                    # if it is in self, but not in other: add it to result unchanged
                    result.append(cur_self_resource_rule)
                    continue

                if isinstance(cur_resource, Resource):
                    # no rule, because it is resolved -> don't need to check rules, element should only be added
                    # if it is not part of the other list (done above)
                    continue

                # if it is in both: add it to other, but change rule to `[self].rule and NOT [other].rule`
                new_resource_rule = cur_self_resource_rule.copy()
                self_rule_cb = cur_self_resource_rule.cb_rule
                other_rule_cb = other_resource_rule.cb_rule

                if self_rule_cb is None and other_rule_cb is None:
                    # do not add this one -> because no rule exists
                    continue

                if other_rule_cb is None:
                    raise ValueError(f'although element `{cur_self_resource_rule}` is part of the list being '
                                     f'subtracted it does not define a more specific rule that the element within '
                                     f'this list')

                def make_updated_callback(the_self_rule, the_other_rule):
                    if the_self_rule is None:
                        return lambda param_list: not other_resource_rule.cb_rule(param_list)
                    return lambda param_list: the_self_rule(param_list) and not the_other_rule(param_list)

                new_resource_rule.update_rule(
                    make_updated_callback(the_self_rule=self_rule_cb, the_other_rule=other_rule_cb)
                )

                result.append(new_resource_rule)
        return ResourceRuleList(result)

    def filter_for_resolved_only(self):
        """
        Filters the list for rules with resolved resources only.

        :return: a new `ResourceRuleList` containing only the rules with resolved resources
        """
        remaining = []
        for rule in self._rules:
            if not isinstance(rule.resource, UnresolvedResource):
                remaining.append(rule)
        return self.__class__(remaining)

    def filter_for_unresolved_only(self):
        """
        Filters the list for rules with unresolved resources only.

        :return: a new `ResourceRuleList` containing only the rules with unresolved resources
        """
        remaining = []
        for rule in self._rules:
            if isinstance(rule.resource, UnresolvedResource):
                remaining.append(rule)
        return self.__class__(remaining)
