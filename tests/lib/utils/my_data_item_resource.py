from typing import Type, Union, Callable

import dataclasses

from balderhub.data.lib.utils import SingleDataItem
from balderhub.data.contrib.auth.utils import ResourceForSpecificDataItem
from tests.lib.utils.my_resource import MyResource


class MyDataItemResource(ResourceForSpecificDataItem):

    @dataclasses.dataclass
    class Parameter(ResourceForSpecificDataItem.Parameter):
        data_item: SingleDataItem

    def __init__(
            self,
            name: str,
            data_item_type: Type[SingleDataItem],
    ):
        super().__init__(data_item_type=data_item_type)
        self._name = name

    def __str__(self):
        return f"{self._name}({self._data_item_type.__name__})"

    def __eq__(self, other):
        return (
            isinstance(other, MyDataItemResource)
            and self._name == other._name
            and self._data_item_type == other._data_item_type
        )

    def __hash__(self):
        return hash((self._name, self._data_item_type))

    @property
    def name(self):
        return self._name

    def get_resolved_resource(self, param: Parameter) -> MyResource:
        unique_id = param.data_item.get_unique_identification()
        return MyResource(f'{self._name}_{unique_id}')
