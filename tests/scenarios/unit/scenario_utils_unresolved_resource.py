from balderhub.unit.scenarios import ScenarioUnit

from balderhub.auth.lib.utils.resource import Resource
from balderhub.auth.lib.utils.unresolved_resource import UnresolvedResource
from tests.scenarios.unit.support import FIRST_RESOURCE, MyParam


class ScenarioUtilsUnresolvedResource(ScenarioUnit):

    def test_str_returns_class_name(self):

        class MyUnresolvedResource(UnresolvedResource):

            def get_resolved_resource(self, param: MyParam) -> Resource:
                return FIRST_RESOURCE

        resource = MyUnresolvedResource()
        assert str(resource) == "MyUnresolvedResource"

    def test_resource_enter_error_is_exception(self):
        assert issubclass(UnresolvedResource.ResourceEnterError, Exception)

    def test_does_not_exist_error_is_resource_enter_error(self):
        assert issubclass(UnresolvedResource.DoesNotExistError, UnresolvedResource.ResourceEnterError)

    def test_unauthorized_error_is_resource_enter_error(self):
        assert issubclass(UnresolvedResource.UnauthorizedError, UnresolvedResource.ResourceEnterError)

    def test_no_permission_error_is_resource_enter_error(self):
        assert issubclass(UnresolvedResource.NoPermissionError, UnresolvedResource.ResourceEnterError)
