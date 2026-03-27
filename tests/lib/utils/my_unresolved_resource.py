from balderhub.auth.lib.utils.unresolved_resource import UnresolvedResource
from balderhub.auth.lib.utils.resource import Resource
from tests.lib.utils.my_resource import MyResource


class MyUnresolvedResource(UnresolvedResource):

    class Parameter(UnresolvedResource.Parameter):
        def __init__(self, item_id: int):
            self._item_id = item_id

        @property
        def item_id(self):
            return self._item_id

        def __eq__(self, other):
            return isinstance(other, MyUnresolvedResource.Parameter) and self._item_id == other._item_id

        def __hash__(self):
            return hash(self._item_id)

        def __repr__(self):
            return f'Parameter(item_id={self._item_id})'

    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, MyUnresolvedResource) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self):
        return self._name

    def get_resolved_resource(self, param: 'MyUnresolvedResource.Parameter') -> Resource:
        return MyResource(f'{self._name}_{param.item_id}')
