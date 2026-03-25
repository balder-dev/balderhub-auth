from balderhub.auth.lib.utils.action import Action


class MyAction(Action):

    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self):
        return self._name


CREATE = MyAction('create')
RETRIEVE = MyAction('retrieve')
UPDATE = MyAction('update')
DELETE = MyAction('delete')
