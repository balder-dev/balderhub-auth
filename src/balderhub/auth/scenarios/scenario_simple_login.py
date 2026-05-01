from __future__ import annotations
import balder

from balderhub.auth.lib.scenario_features.client import UserLoginFeature
from balderhub.auth.lib.scenario_features.client.role import UserRoleFeature


class ScenarioSimpleLogin(balder.Scenario):
    """
    This is a simple scenario that evaluates if a user can be logged in.
    """

    class Client(balder.Device):
        """
        client device where the login can be executed
        """
        role = UserRoleFeature()
        login = UserLoginFeature()

    def test_login(self):
        """
        This test executes a simple login and validates if the login succeeds.
        """
        assert not self.Client.login.is_already_logged_in(), "a user was already logged in"

        self.Client.login.insert_username(self.Client.role.username)
        self.Client.login.insert_password(self.Client.role.password)

        self.Client.login.submit_login()

        assert self.Client.login.is_already_logged_in(), "login failed because no user has been logged in"
