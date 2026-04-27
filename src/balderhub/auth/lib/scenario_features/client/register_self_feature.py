import balder

from balderhub.auth.lib.scenario_features.client.role import UserRoleFeature


class RegisterSelfFeature(balder.Feature):
    """
    This feature can be assigned to devices that can register their own role.
    """
    role = UserRoleFeature()

    def register(self) -> None:
        """
        Registers the client this feature is assigned to, specified by the role.
        """
        raise NotImplementedError
