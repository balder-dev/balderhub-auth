from balderhub.unit.scenarios import ScenarioUnit

from balderhub.auth.lib.utils.resource_rule import ResourceRule
from balderhub.auth.lib.utils.resource_rule_list import ResourceRuleList
from tests.scenarios.unit.support import FIRST_RESOURCE, FIRST_ACTION, SECOND_ACTION, SECOND_RESOURCE, THIRD_ACTION, \
    MyUnresolvedResource, MyParam


class ScenarioUtilsResourceRuleList(ScenarioUnit):

    def test_create_empty_resource_rule_list(self):
        rrl = ResourceRuleList()
        assert isinstance(rrl, ResourceRuleList)
        assert list(rrl) == []

    def test_create_with_iterable(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl = ResourceRuleList([rule])
        items = list(rrl)
        assert len(items) == 1
        assert items[0] is rule

    def test_rules_property(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl = ResourceRuleList([rule])
        assert rrl.rules == [rule]

    def test_append_valid_rule(self):
        rrl = ResourceRuleList()
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl.append(rule)
        assert list(rrl) == [rule]

    def test_append_raises_type_error_for_non_rule(self):
        rrl = ResourceRuleList()
        try:
            rrl.append("not_a_rule")
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "rule must be an instance of `ResourceRule`", exc

    def test_append_raises_value_error_for_duplicate(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl = ResourceRuleList([rule])
        try:
            rrl.append(rule)
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert exc.args[0] == "object `ResourceRule<MyResource<1>:['MyAction<FIRST_ACTION>']>` can not be added multiple times", exc

    def test_extend_valid(self):
        rule1 = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rule2 = ResourceRule(resource=SECOND_RESOURCE, actions=[SECOND_ACTION])
        rrl1 = ResourceRuleList([rule1])
        rrl2 = ResourceRuleList([rule2])
        rrl1.extend(rrl2)
        assert len(rrl1) == 2
        assert len(rrl2) == 1

    def test_extend_skips_duplicates(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl1 = ResourceRuleList([rule])
        rrl2 = ResourceRuleList([rule])
        rrl1.extend(rrl2)
        assert len(rrl1) == 1
        assert rrl1 == rrl2

    def test_extend_raises_type_error_for_non_list(self):
        rrl = ResourceRuleList()
        try:
            rrl.extend("not_a_list")
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "object must be an instance of `ResourceRuleList`", exc

    def test_iter(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl = ResourceRuleList([rule])
        items = [r for r in rrl]
        assert items == [rule]

    def test_flatten(self):
        my_action = FIRST_ACTION
        another_action = SECOND_ACTION
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[my_action, another_action])
        rrl = ResourceRuleList([rule])
        flattened = rrl.flatten()
        assert isinstance(flattened, ResourceRuleList)
        assert len(flattened) == 2
        for item in flattened:
            assert len(item.actions) == 1
        assert ResourceRule(resource=FIRST_RESOURCE, actions=[my_action]) in flattened
        assert ResourceRule(resource=FIRST_RESOURCE, actions=[another_action]) in flattened

    def test_flatten_single_action(self):
        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl = ResourceRuleList([rule])
        flattened = rrl.flatten()
        items = list(flattened)
        assert len(items) == 1
        assert rule == items[0]

    def test_flatten_and_group_by_resource_and_action(self):

        rule = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION, SECOND_ACTION])
        rule2 = ResourceRule(resource=FIRST_RESOURCE, actions=[THIRD_ACTION])
        rrl = ResourceRuleList([rule, rule2])
        grouped = rrl.flatten_and_group_by_resource_and_action()

        assert len(grouped) == 1
        assert FIRST_RESOURCE == list(grouped.keys())[0]
        assert len(grouped[FIRST_RESOURCE]) == 3
        assert FIRST_ACTION in grouped[FIRST_RESOURCE]
        assert SECOND_ACTION in grouped[FIRST_RESOURCE]
        assert THIRD_ACTION in grouped[FIRST_RESOURCE]

    def test_sub_resolved_removes_matching(self):

        rule_self = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION, SECOND_ACTION])
        rule_other = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rrl_self = ResourceRuleList([rule_self])
        rrl_other = ResourceRuleList([rule_other])
        result = rrl_self - rrl_other
        assert isinstance(result, ResourceRuleList)
        items = list(result)
        assert len(items) == 1
        assert items[0].resource is FIRST_RESOURCE
        assert items[0].actions[0] is SECOND_ACTION

    def test_sub_raises_type_error_for_non_list(self):
        rrl = ResourceRuleList()
        try:
            rrl - "not_a_list"
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "object must be an instance of `ResourceRuleList`", exc

    def test_sub_raises_value_error_for_missing_element(self):
        rule_self = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rule_other = ResourceRule(resource=SECOND_RESOURCE, actions=[SECOND_ACTION])
        rrl_self = ResourceRuleList([rule_self])
        rrl_other = ResourceRuleList([rule_other])
        try:
            rrl_self - rrl_other
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert exc.args[0] == "element `ResourceRule<MyResource<2>:['MyAction<SECOND_ACTION>']>` from the list being subtracted is not present in the current list", exc

    def test_sub_empty_minus_empty(self):
        result = ResourceRuleList() - ResourceRuleList()
        assert list(result) == []

    def test_sub_unresolved_combines_rules(self):
        resource = MyUnresolvedResource('first')
        rule_self = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: True)
        rule_other = ResourceRule(resource=resource, actions=[FIRST_ACTION], rule=lambda p: False)
        rrl_self = ResourceRuleList([rule_self])
        rrl_other = ResourceRuleList([rule_other])
        result = rrl_self - rrl_other
        items = list(result)
        assert len(items) == 1
        param = MyParam('temp')
        assert items[0].cb_rule(param) is True

    def test_filter_for_resolved_only(self):
        unresolved = MyUnresolvedResource('temp')
        rule1 = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rule2 = ResourceRule(resource=unresolved, actions=[SECOND_ACTION], rule=lambda p: True)
        rrl = ResourceRuleList([rule1, rule2])
        filtered = rrl.filter_for_resolved_only()
        assert isinstance(filtered, ResourceRuleList)
        items = list(filtered)
        assert len(items) == 1
        assert items[0].resource is FIRST_RESOURCE

    def test_filter_for_unresolved_only(self):
        unresolved = MyUnresolvedResource('temp')
        rule1 = ResourceRule(resource=FIRST_RESOURCE, actions=[FIRST_ACTION])
        rule2 = ResourceRule(resource=unresolved, actions=[SECOND_ACTION], rule=lambda p: True)
        rrl = ResourceRuleList([rule1, rule2])
        filtered = rrl.filter_for_unresolved_only()
        assert isinstance(filtered, ResourceRuleList)
        items = list(filtered)
        assert len(items) == 1
        assert items[0].resource is unresolved
