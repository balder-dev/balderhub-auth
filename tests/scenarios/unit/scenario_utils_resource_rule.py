from balderhub.unit.scenarios import ScenarioUnit

from balderhub.auth.lib.utils.operation import Operation
from balderhub.auth.lib.utils.operation_list import OperationList
from balderhub.auth.lib.utils.resource_rule import ResourceRule
from tests.scenarios.unit.support import FIRST_RESOURCE, FIRST_ACTION, MyUnresolvedResource, SECOND_ACTION, MyParam, \
    MyResolvedResource


class ScenarioUtilsResourceRule(ScenarioUnit):

    def test_create_resource_rule_with_resource(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        assert isinstance(rule, ResourceRule)

    def test_create_resource_rule_with_unresolved_resource(self):
        resource = MyUnresolvedResource('temp')
        rule = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: True)
        assert isinstance(rule, ResourceRule)

    def test_resource_property(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        assert rule.resource is FIRST_RESOURCE, rule.resource
        assert isinstance(rule.actions, list), rule.actions
        assert len(rule.actions) == 1 and rule.actions[0] is FIRST_ACTION, rule.actions

    def test_actions_property_returns_copy(self):
        actions = [FIRST_ACTION, SECOND_ACTION]
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=actions)
        returned = rule.actions
        assert returned == actions
        assert returned is not actions

    def test_cb_rule_property_none_by_default(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        assert rule.cb_rule is None

    def test_cb_rule_property_returns_callable(self):
        resource = MyUnresolvedResource('temp')
        my_rule = lambda p: True
        rule = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=my_rule)
        assert rule.cb_rule is my_rule

    def test_raises_value_error_rule_with_resolved_resource(self):
        try:
            ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION], rule=lambda p: True)
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert exc.args[0] == 'rules can only be provided for unresolved resources', exc

    def test_str_contains_class_name(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        result = str(rule)
        assert 'ResourceRule' in result

    def test_copy_returns_new_instance(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        copied = rule.copy()
        assert isinstance(copied, ResourceRule)
        assert copied is not rule

    def test_update_rule(self):
        resource = MyUnresolvedResource('temp')
        rule = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: True)
        new_rule = lambda p: False
        rule.update_rule(new_rule)
        assert rule.cb_rule is new_rule

    def test_update_rule_to_none(self):
        resource = MyUnresolvedResource('temp')
        rule = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: True)
        rule.update_rule(None)
        assert rule.cb_rule is None

    def test_flatten_returns_resource_rule_list(self):
        from balderhub.auth.lib.utils.resource_rule_list import ResourceRuleList

        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION, SECOND_ACTION])
        flattened = rule.flatten()
        assert isinstance(flattened, ResourceRuleList)
        items = list(flattened)
        assert len(items) == 2
        assert ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION]) in items
        assert ResourceRule(resource=FIRST_RESOURCE, actions=[SECOND_ACTION]) in items

    def test_flatten_single_action(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        flattened = rule.flatten()
        items = list(flattened)
        assert len(items) == 1
        assert rule == items[0]

    def test_resolve_with_resource_returns_operation_list(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION, SECOND_ACTION])
        result = rule.resolve()
        assert isinstance(result, OperationList)
        ops = list(result)
        assert len(ops) == 2
        assert Operation(FIRST_RESOURCE, FIRST_ACTION) in ops
        assert Operation(FIRST_RESOURCE, SECOND_ACTION) in ops

    def test_resolve_with_unresolved_resource_matching_rule(self):
        resource = MyUnresolvedResource('temp')
        rule = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: True)
        param = MyParam('123')
        result = rule.resolve(parameter=param)
        assert isinstance(result, OperationList)
        ops = list(result)
        assert len(ops) == 1
        assert Operation(MyResolvedResource('temp[123]'), action=FIRST_ACTION) == ops[0]

    def test_resolve_with_unresolved_resource_non_matching_rule(self):
        resource = MyUnresolvedResource('temp')
        rule = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: False)
        param = MyParam('123')
        result = rule.resolve(parameter=param)
        assert result is None

    def test_resolve_raises_value_error_param_with_resolved_resource(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        param = MyParam('temp')
        try:
            rule.resolve(parameter=param)
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert exc.args[0] == 'parameters can only be provided for unresolved resources', exc

    def test_resolve_raises_value_error_for_non_bool_rule(self):
        resource = MyUnresolvedResource('temp')
        rule = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: "yes")
        param = MyParam('123')
        try:
            rule.resolve(parameter=param)
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert exc.args[0] == 'unexpected return value of rule function: `yes` - should be a boolean value', exc
