from balderhub.auth.lib.utils.resource import Resource


class MyResource(Resource):

    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self._name

    def __hash__(self):
        return hash(self.name)
