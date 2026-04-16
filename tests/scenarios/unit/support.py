
from balderhub.auth.lib.utils.action import Action
from balderhub.auth.lib.utils.resource import Resource
from balderhub.auth.lib.utils.unresolved_resource import UnresolvedResource


class MyResource(Resource):

    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return f"{self.__class__.__name__}<{self._name}>"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._name == other._name

    def __hash__(self):
        return hash(self.__class__) + hash(self._name)

class MyAction(Action):
    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return f"MyAction<{self._name}>"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._name == other._name

    def __hash__(self):
        return hash(self.__class__) + hash(self._name)

class MyResolvedResource(MyResource):
    pass


class MyParam(UnresolvedResource.Parameter):
    def __init__(self, val: str, **kwargs):
        super().__init__(**kwargs)
        self._val = val

    @property
    def val(self):
        return self._val


class MyUnresolvedResource(UnresolvedResource):

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self._name = name

    def __str__(self):
        return f"MyUnresolvedResource<{self._name}>"

    def get_resolved_resource(self, param: MyParam) -> Resource:
        return MyResolvedResource(f"{self._name}[{param.val}]")


FIRST_RESOURCE = MyResource('1')
SECOND_RESOURCE = MyResource('2')
THIRD_RESOURCE = MyResource('3')

FIRST_ACTION = MyAction('FIRST_ACTION')
SECOND_ACTION = MyAction('SECOND_ACTION')
THIRD_ACTION = MyAction('THIRD_ACTION')
