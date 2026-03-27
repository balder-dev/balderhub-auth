from balderhub.auth.lib.scenario_features.client.unresolved_resource_parameter_config import UnresolvedResourceParameterConfig
from balderhub.auth.lib.utils.unresolved_resource import UnresolvedResource
from tests.lib.utils.my_data_item_resource import MyDataItemResource
from tests.lib.utils.data_items.book_data_item import BookDataItem
from tests.lib.utils.data_items.author_data_item import AuthorDataItem
from tests.lib.setup_features.client.data_item_dut_manager_feature import (
    AUTHOR_1, AUTHOR_2, AUTHOR_3, BOOK_1, BOOK_2, BOOK_3,
)


class DataItemUnresolvedParamConfig(UnresolvedResourceParameterConfig):
    """Provides parameters for data-item-based unresolved resources used in tests."""

    def get_parameters_for(self, resource_rule) -> list[UnresolvedResource.Parameter]:
        resource = resource_rule.resource
        if isinstance(resource, MyDataItemResource):
            if resource.data_item_type == BookDataItem:
                return [
                    MyDataItemResource.Parameter(data_item=BOOK_1),
                    MyDataItemResource.Parameter(data_item=BOOK_2),
                    MyDataItemResource.Parameter(data_item=BOOK_3),
                ]
            elif resource.data_item_type == AuthorDataItem:
                return [
                    MyDataItemResource.Parameter(data_item=AUTHOR_1),
                    MyDataItemResource.Parameter(data_item=AUTHOR_2),
                    MyDataItemResource.Parameter(data_item=AUTHOR_3),
                ]
        return []
