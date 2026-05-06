import logging
import balder
from ..lib import scenario_features


logger = logging.getLogger(__name__)


class ScenarioRegisterNewAsUnauth(balder.Scenario):
    """
    Represents the scenario for registering a new user as an unauthenticated client.

    The purpose of this class is to test the workflow of registering a user who is
    unauthenticated and validate the login process before and after the registration. It consists
    of a `Server` device that provides resources and an `UnauthClient` device that performs the
    registration and login process.
    """

    class UnauthClient(balder.Device):
        """the unauthenticated client device that registers itself"""
        #: user role describing username and password
        role = scenario_features.client.role.UserRoleFeature()
        #: login feature allowing to perform the login process
        login = scenario_features.client.UserLoginFeature()
        #: feature for registering the user
        register_user = scenario_features.client.RegisterSelfFeature()

    def test_register_new_user(self) -> None:
        """
        Tests the functionality of registering a new user as an unauthenticated user
        and validates the login process for a new user before and after registration.
        """
        assert not self.UnauthClient.login.is_already_logged_in(), \
            "user, that should be registered, is already logged in"

        logger.info('try to log in user before registration (should fail)')
        self.UnauthClient.login.insert_username(self.UnauthClient.role.username)
        self.UnauthClient.login.insert_password(self.UnauthClient.role.password)
        self.UnauthClient.login.submit_login()

        assert not self.UnauthClient.login.is_already_logged_in(), \
            "user can log in before registration"
        logger.info('log in of user before registration failed like expected')

        logger.info('now register new user with unauthenticated client')
        self.UnauthClient.register_user.register()

        logger.info('now try to login with newly registered user')
        self.UnauthClient.login.insert_username(self.UnauthClient.role.username)
        self.UnauthClient.login.insert_password(self.UnauthClient.role.password)
        self.UnauthClient.login.submit_login()
        assert self.UnauthClient.login.is_already_logged_in(), \
            "user was not able to login after registration -> should be possible"
        logger.info('login with new user was possible like expected')
