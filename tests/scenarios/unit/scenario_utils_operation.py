from balderhub.unit.scenarios import ScenarioUnit

from balderhub.auth.lib.utils.action import Action
from balderhub.auth.lib.utils.resource import Resource
from balderhub.auth.lib.utils.operation import Operation
from tests.scenarios.unit.support import FIRST_RESOURCE, FIRST_ACTION


class ScenarioUtilsOperation(ScenarioUnit):

    def test_create_operation_with_valid_args(self):
        op = Operation(resource=FIRST_RESOURCE, action=FIRST_ACTION)
        assert isinstance(op, Operation)
        assert op.action is FIRST_ACTION
        assert op.resource is FIRST_RESOURCE

    def test_raises_type_error_for_invalid_resource(self):
        try:
            Operation(resource="not_a_resource", action=FIRST_ACTION)
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "resource must be of type Resource", exc

    def test_raises_type_error_for_invalid_action(self):
        try:
            Operation(resource=FIRST_RESOURCE, action="not_an_action")
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "action must be of type Action", exc

    def test_raises_type_error_for_none_resource(self):
        try:
            Operation(resource=None, action=FIRST_ACTION)
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "resource must be of type Resource", exc

    def test_raises_type_error_for_none_action(self):
        try:
            Operation(resource=FIRST_RESOURCE, action=None)
            assert False, "Expected TypeError"
        except TypeError as exc:
            assert exc.args[0] == "action must be of type Action", exc

    def test_does_not_exist_error_is_operation_enter_error(self):
        assert issubclass(Operation.DoesNotExistError, Operation.OperationEnterError)

    def test_unauthorized_error_is_operation_enter_error(self):
        assert issubclass(Operation.UnauthorizedError, Operation.OperationEnterError)

    def test_no_permission_error_is_operation_enter_error(self):
        assert issubclass(Operation.NoPermissionError, Operation.OperationEnterError)

    def test_operation_enter_error_is_exception(self):
        assert issubclass(Operation.OperationEnterError, Exception)
