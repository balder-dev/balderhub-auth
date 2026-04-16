from __future__ import annotations
from typing import Union, Callable, TYPE_CHECKING
import copy

from .resource import Resource

from .unresolved_resource import UnresolvedResource
from .operation import Operation
from .operation_list import OperationList
from .action import Action

if TYPE_CHECKING:
    from .resource_rule_list import ResourceRuleList


class ResourceRule:
    """
    This class represents a rule for a resource and a list of actions that are allowed for this resource.
    """
    # TODO should we provide two different objects??
    def __init__(
            self,
            resource: Union[Resource, UnresolvedResource],
            actions: list[Action],
            rule: Union[Callable[[UnresolvedResource.Parameter], bool], None] = None
    ):
        """
        :param resource: the resource the rule is for
        :param actions: a list of actions that are allowed for this resource
        :param rule: an optional rule function that is used to check if the actions are allowed for a specific
                     parameter of an unresolved resource
        """
        if rule is not None and not isinstance(resource, UnresolvedResource):
            raise ValueError('rules can only be provided for unresolved resources')

        self._resource = resource
        self._actions = actions
        self._rule = rule

    def __str__(self):
        return f'{self.__class__.__name__}<{self.resource}:{[str(action) for action in self.actions]}>'

    def __eq__(self, other: ResourceRule):
        if not isinstance(other, ResourceRule):
            return False
        if self.resource != other.resource:
            return False
        if set(self.actions) != set(other.actions):
            return False
        if self.cb_rule is not None and other.cb_rule is not None:
            if callable(self.cb_rule) and callable(other.cb_rule):
                return self.cb_rule.__code__.co_code == other.cb_rule.__code__.co_code
            return False
        return True

    @property
    def resource(self) -> Union[Resource, UnresolvedResource]:
        """returns the resource of this rule"""
        return self._resource

    @property
    def actions(self) -> list[Action]:
        """returns a copy of the list of actions of this rule"""
        return self._actions.copy()

    @property
    def cb_rule(self) -> Union[Callable[[UnresolvedResource.Parameter], bool], None]:
        """returns the rule callback of this rule"""
        return self._rule

    def copy(self) -> ResourceRule:
        """creates a deep copy of this rule"""
        return copy.deepcopy(self)

    def update_rule(self, new_rule: Union[Callable[[UnresolvedResource.Parameter], bool], None]) -> None:
        """updates the rule callback of this rule"""
        self._rule = new_rule

    def flatten(self) -> ResourceRuleList:
        """
        Converts this rule into a ResourceRuleList where every ResourceRule has exactly one Action.

        :return: a ResourceRuleList containing the flattened rules
        """
        from .resource_rule_list import ResourceRuleList  # pylint: disable=import-outside-toplevel
        result = []
        for cur_action in self._actions:
            result.append(ResourceRule(resource=self._resource, actions=[cur_action], rule=self._rule))
        return ResourceRuleList(result)

    def resolve(self, parameter: Union[UnresolvedResource.Parameter, None] = None) -> Union[OperationList, None]:
        """
        Resolves the rule with the given parameter.

        If the resource is a resolved resource, the parameter must be None. If the resource is an unresolved resource,
        the parameter can be provided. If a parameter is provided, the rule function is called with the parameter. If
        the rule function returns False, None is returned. Otherwise, the unresolved resource is resolved with the
        parameter and an OperationList containing the resolved resource and the actions is returned.

        :param parameter: the parameter for the unresolved resource
        :return: an OperationList containing the resolved operations or None if the rule does not match
        """
        if parameter is None:
            if isinstance(self._resource, UnresolvedResource):
                raise TypeError(f'can not resolve an `{self._resource.__class__.__name__}` without a '
                                f'parameter - please provide parameters for rules with unresolved resources')
            return OperationList([Operation(resource=self._resource, action=action) for action in self._actions])

        if not isinstance(self._resource, UnresolvedResource):
            raise ValueError('parameters can only be provided for unresolved resources')

        match_rule = self._rule(parameter)
        if not isinstance(match_rule, bool):
            raise ValueError(f'unexpected return value of rule function: `{match_rule}` - should be a boolean value')
        if not match_rule:
            return None

        result = OperationList()

        resolved_resource = self._resource.get_resolved_resource(parameter)
        for cur_action in self._actions:
            result.append(Operation(resolved_resource, cur_action))
        return result
