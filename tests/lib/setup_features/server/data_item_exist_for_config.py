import balderhub.auth.lib.scenario_features
from balderhub.auth.lib.utils import ResourceRule, ResourceRuleList
from tests.lib.utils.my_resource import MyResource
from tests.lib.utils.my_data_item_resource import MyDataItemResource
from tests.lib.utils import my_action
from tests.lib.utils.data_items.book_data_item import BookDataItem
from tests.lib.utils.data_items.author_data_item import AuthorDataItem


class DataItemExistForConfig(balderhub.auth.lib.scenario_features.server.ExistenceForConfig):
    """Provides the existence configuration for data-item-based resources."""

    def get_resource_rules_that_exist(self) -> ResourceRuleList:
        result = ResourceRuleList()
        result.append(ResourceRule(resource=MyResource('catalog'), actions=[my_action.RETRIEVE]))
        result.append(ResourceRule(
            resource=MyDataItemResource('books', BookDataItem),
            actions=[my_action.RETRIEVE, my_action.UPDATE, my_action.DELETE],
            rule=lambda param: param.data_item.id in [1, 2, 3]
        ))
        result.append(ResourceRule(
            resource=MyDataItemResource('authors', AuthorDataItem),
            actions=[my_action.RETRIEVE, my_action.UPDATE],
            rule=lambda param: param.data_item.id in [1, 2, 3]
        ))
        return result

    def get_resource_rules_that_not_exist(self) -> ResourceRuleList:
        result = ResourceRuleList()
        result.append(ResourceRule(resource=MyResource('nonexistent_catalog'), actions=[my_action.RETRIEVE]))
        result.append(ResourceRule(
            resource=MyDataItemResource('books', BookDataItem),
            actions=[my_action.RETRIEVE],
            rule=lambda param: param.data_item.id not in [1, 2, 3]
        ))
        result.append(ResourceRule(
            resource=MyDataItemResource('authors', AuthorDataItem),
            actions=[my_action.RETRIEVE],
            rule=lambda param: param.data_item.id not in [1, 2, 3]
        ))
        return result
