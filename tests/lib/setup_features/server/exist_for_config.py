import balderhub.auth.lib.scenario_features
from balderhub.auth.lib.utils import ResourceRule, ResourceRuleList
from ...utils.my_resource import MyResource
from ...utils.my_unresolved_resource import MyUnresolvedResource
from ...utils import my_action


class ExistForConfig(balderhub.auth.lib.scenario_features.server.ExistenceForConfig):
    """Provides the existence configuration for resolved and unresolved resources."""

    def get_resource_rules_that_exist(self) -> ResourceRuleList:
        result = ResourceRuleList()
        result.append(ResourceRule(resource=MyResource('articles'), actions=[my_action.RETRIEVE, my_action.CREATE, my_action.DELETE]))
        result.append(ResourceRule(resource=MyResource('users'), actions=[my_action.RETRIEVE, my_action.CREATE]))
        result.append(ResourceRule(resource=MyResource('public'), actions=[my_action.RETRIEVE]))
        result.append(ResourceRule(
            resource=MyUnresolvedResource('items'),
            actions=[my_action.RETRIEVE, my_action.UPDATE, my_action.DELETE],
            rule=lambda param: param.item_id in [1, 2, 3]
        ))
        return result

    def get_resource_rules_that_not_exist(self) -> ResourceRuleList:
        result = ResourceRuleList()
        result.append(ResourceRule(resource=MyResource('nonexistent'), actions=[my_action.RETRIEVE, my_action.CREATE]))
        result.append(ResourceRule(
            resource=MyUnresolvedResource('items'),
            actions=[my_action.RETRIEVE],
            rule=lambda param: param.item_id not in [1, 2, 3]
        ))
        return result
