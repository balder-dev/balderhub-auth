import balder

from balderhub.auth.lib.utils import UnresolvedResource
from balderhub.auth.lib.utils.global_resource_config import GlobalResourceConfig, Usergroup, \
    GlobalUnresolvedResourceConfig
from tests.lib.utils.my_endpoint_resource import MyResource


class GlobalAuthConfig(balder.Feature):

    class Superuser(Usergroup):
        pass

    class Api(Usergroup):
        pass

    def config(self):
        return [
            GlobalResourceConfig(
                resource=MyResource('login'),
                existing_actions=['Get', 'POST'],
                auth_required_actions=['POST', 'DELETE']
            ).add_perm_for_usergroup(self.Superuser, ['POST', 'DELETE']),

            GlobalUnresolvedResourceConfig(
                resource=UnresolvedResource('book'),
                existing_actions=['GET', 'POST'],
                auth_required_actions=['POST', 'DELETE']
            )
            .add_perm_for_usergroup(self.Superuser, ['GET', 'POST'], rule=lambda params: params)
            .add_perm_for_usergroup(self.Api, ['POST', 'DELETE'], rule=lambda params: [p for p in params if p.public])
        ]