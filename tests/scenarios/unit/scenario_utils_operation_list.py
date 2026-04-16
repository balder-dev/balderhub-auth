from balderhub.unit.scenarios import ScenarioUnit


from balderhub.auth.lib.utils.operation import Operation
from balderhub.auth.lib.utils.operation_list import OperationList
from tests.scenarios.unit.support import FIRST_RESOURCE, FIRST_ACTION, SECOND_ACTION


class ScenarioUtilsOperationList(ScenarioUnit):

    def test_create_empty_operation_list(self):
        op_list = OperationList()
        assert list(op_list) == []

    def test_create_operation_list_with_iterable(self):
        op1 = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op2 = Operation(resource=FIRST_RESOURCE, action=SECOND_ACTION)
        op_list = OperationList([op1, op2])
        assert list(op_list) == [op1, op2]

    def test_append_operation(self):
        op_list = OperationList()
        op = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op_list.append(op)
        assert list(op_list) == [op]

    def test_append_raises_type_error_for_non_operation(self):
        op_list = OperationList()
        try:
            op_list.append("not_an_operation")
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "Operation must be an instance of `Operation`", exc

    def test_append_raises_value_error_for_duplicate(self):
        op = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op_list = OperationList([op])
        try:
            op_list.append(op)
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert exc.args[0] == "object `Operation<MyResource<1>:['MyAction<FIRST_ACTION>']>` can not be added multiple times", exc

    def test_extend_with_operation_list(self):
        op1 = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op2 = Operation(resource=FIRST_RESOURCE, action=SECOND_ACTION)
        list1 = OperationList([op1])
        list2 = OperationList([op2])
        list1.extend(list2)
        assert list(list1) == [op1, op2]

    def test_extend_skips_duplicates(self):
        op1 = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op2 = Operation(resource=FIRST_RESOURCE, action=SECOND_ACTION)
        list1 = OperationList([op1, op2])
        list2 = OperationList([op1])
        list1.extend(list2)
        assert list(list1) == [op1, op2]

    def test_extend_raises_type_error_for_non_operation_list(self):
        op_list = OperationList()
        try:
            op_list.extend([])
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "object must be an instance of `OperationList`", exc

    def test_sub_returns_new_operation_list(self):
        op1 = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op2 = Operation(resource=FIRST_RESOURCE, action=SECOND_ACTION)
        list1 = OperationList([op1, op2])
        list2 = OperationList([op1])
        result = list1 - list2
        assert list(result) == [op2]
        # original unchanged
        assert list(list1) == [op1, op2], list(list1)
        assert list(list2) == [op1], list(list2)

    def test_sub_raises_type_error_for_non_operation_list(self):
        op_list = OperationList()
        try:
            _ = op_list - []
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "object must be an instance of `OperationList`", exc

    def test_sub_raises_value_error_for_missing_element(self):
        op1 = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op2 = Operation(resource=FIRST_RESOURCE, action=SECOND_ACTION)
        list1 = OperationList([op1])
        list2 = OperationList([op2])
        try:
            _ = list1 - list2
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert exc.args[0] == ("element `Operation<MyResource<1>:['MyAction<SECOND_ACTION>']>` from the list being "
                                   "subtracted is not present in the current list"), exc

    def test_iter(self):
        op1 = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        op2 = Operation(resource=FIRST_RESOURCE, action=SECOND_ACTION)
        op_list = OperationList([op1, op2])
        items = [item for item in op_list]
        assert items == [op1, op2]

    def test_sub_empty_from_empty(self):
        result = OperationList() - OperationList()
        assert list(result) == [], result
