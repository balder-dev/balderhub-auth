import balderhub.auth.lib.setup_features
from balderhub.auth.lib.utils import ResourceRule, ResourceRuleList
from tests.lib.utils.my_data_item_resource import MyDataItemResource
from tests.lib.utils import my_action
from tests.lib.utils.data_items.book_data_item import BookDataItem
from tests.lib.utils.data_items.author_data_item import AuthorDataItem


class DataItemAuthForConfig(balderhub.auth.lib.setup_features.server.AuthenticationForConfig):
    """Provides the authentication configuration for data-item-based resources."""

    def get_resource_rules_that_require_authentication(self) -> ResourceRuleList:
        result = ResourceRuleList()
        result.append(ResourceRule(
            resource=MyDataItemResource('books', BookDataItem),
            actions=[my_action.RETRIEVE, my_action.UPDATE, my_action.DELETE],
            rule=lambda param: True
        ))
        result.append(ResourceRule(
            resource=MyDataItemResource('authors', AuthorDataItem),
            actions=[my_action.RETRIEVE, my_action.UPDATE],
            rule=lambda param: True
        ))
        return result
