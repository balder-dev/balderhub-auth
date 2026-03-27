import balderhub.auth.lib.setup_features
from balderhub.auth.lib.utils import ResourceRule, ResourceRuleList
from ...utils.my_resource import MyResource
from ...utils.my_unresolved_resource import MyUnresolvedResource
from ...utils import my_action


class AuthForConfig(balderhub.auth.lib.setup_features.server.AuthenticationForConfig):
    """Provides the authentication configuration for resolved and unresolved resources."""

    def get_resource_rules_that_require_authentication(self) -> ResourceRuleList:
        result = ResourceRuleList()
        result.append(ResourceRule(resource=MyResource('articles'), actions=[my_action.CREATE, my_action.RETRIEVE, my_action.DELETE]))
        result.append(ResourceRule(resource=MyResource('users'), actions=[my_action.CREATE, my_action.RETRIEVE]))
        result.append(ResourceRule(
            resource=MyUnresolvedResource('items'),
            actions=[my_action.RETRIEVE, my_action.UPDATE, my_action.DELETE],
            rule=lambda param: True
        ))
        return result
