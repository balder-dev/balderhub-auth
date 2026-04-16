from balderhub.unit.scenarios import ScenarioUnit

from balderhub.auth.lib.utils.resource import Resource


class MyResource(Resource):
    pass


class ScenarioUtilsResource(ScenarioUnit):

    def test_str_returns_class_name(self):
        resource = MyResource()
        assert str(resource) == "MyResource"

    def test_resource_enter_error_is_exception(self):
        assert issubclass(Resource.ResourceEnterError, Exception)

    def test_does_not_exist_error_is_resource_enter_error(self):
        assert issubclass(Resource.DoesNotExistError, Resource.ResourceEnterError)

    def test_unauthorized_error_is_resource_enter_error(self):
        assert issubclass(Resource.UnauthorizedError, Resource.ResourceEnterError)

    def test_no_permission_error_is_resource_enter_error(self):
        assert issubclass(Resource.NoPermissionError, Resource.ResourceEnterError)
