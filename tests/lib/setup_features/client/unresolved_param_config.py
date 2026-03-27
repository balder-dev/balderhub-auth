from balderhub.auth.lib.scenario_features.client.unresolved_resource_parameter_config import UnresolvedResourceParameterConfig
from balderhub.auth.lib.utils.unresolved_resource import UnresolvedResource
from tests.lib.utils.my_unresolved_resource import MyUnresolvedResource


class UnresolvedParamConfig(UnresolvedResourceParameterConfig):
    """Provides parameters for unresolved resources used in tests."""

    def get_parameters_for(self, resource_rule) -> list[UnresolvedResource.Parameter]:
        return [
            MyUnresolvedResource.Parameter(1),
            MyUnresolvedResource.Parameter(2),
            MyUnresolvedResource.Parameter(3),
        ]
