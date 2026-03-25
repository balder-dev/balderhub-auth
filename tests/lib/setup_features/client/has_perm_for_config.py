import balderhub.auth.lib.setup_features
from balderhub.auth.lib.utils import ResourceRule, ResourceRuleList

from tests.lib.utils.my_resource import MyResource
from tests.lib.utils import my_action


class HasPermForConfig(balderhub.auth.lib.setup_features.client.HasPermissionsForConfig):
    """Provides the permission configuration for resolved resources."""

    def get_resource_rules_with_permissions(self) -> ResourceRuleList:
        result = ResourceRuleList()
        result.append(ResourceRule(resource=MyResource('articles'), actions=[my_action.RETRIEVE, my_action.CREATE]))
        result.append(ResourceRule(resource=MyResource('users'), actions=[my_action.RETRIEVE]))
        return result
