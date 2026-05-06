import logging
import balder
from ..lib import scenario_features

logger = logging.getLogger(__file__)


class ScenarioPasswordResetWithOtherAuth(balder.Scenario):
    """
    Scenario for resetting a user's password with the involvement of another client.

    This scenario outlines the process for securely resetting a user's password
    through interactions between a Master Client and a Slave Client, as well as
    confirming the reset process and validating the new password.

    .. image:: /_static/ScenarioPasswordResetWithOtherAuth.svg
        :align: center
        :alt: Visual Description of this ``ScenarioPasswordResetWithOtherAuth``


    """
    class Server(balder.Device):
        """the server device that provides the resources"""

    @balder.connect(Server, balder.Connection())  # pylint: disable=undefined-variable
    class MasterClient(balder.Device):
        """
        The client device that initiates and manages the password
        reset process for another user, while ensuring authentication security.
        """
        #: state machine for the authentication
        sm_auth = scenario_features.client.AuthenticationStateMachine()
        #: feature for resetting the password for another user
        password_reset = scenario_features.client.PasswordResetForOtherUserFeature()

    @balder.connect(Server, balder.Connection())  # pylint: disable=undefined-variable
    class SlaveClient(balder.Device):
        """
        The client device associated with the user whose password
        will be reset. Handles login, logout, and second-factor-based reset
        confirmation.
        """
        #: user role describing username and password
        role = scenario_features.client.role.UserRoleFeature()
        #: login feature allowing to perform the login process
        login = scenario_features.client.UserLoginFeature()
        #: logout feature allowing to perform the logout process
        logout = scenario_features.client.UserLogoutFeature()
        #: provider for password field values
        passwd_provider = scenario_features.client.PasswordFieldValueProvider()
        #: feature for resetting the password
        password_reset = scenario_features.client.PasswordResetFeature()

    def test_password_reset(self):
        """
        Tests the password reset functionality to ensure that a user can reset their
        password, confirm the reset via a secondary factor, and successfully log in
        with the new password while being denied access with the old password.

        The test validates multiple authentication scenarios during and after the
        password reset process to confirm correct behavior. The old password should
        become invalid after the reset, and the new password should grant access.
        """
        new_password = self.SlaveClient.passwd_provider.get_primary_valid_password().value

        logger.info('make sure that user is not logged in')
        assert not self.SlaveClient.login.is_already_logged_in(), "user is logged in after confirmed password reset"

        logger.info('try to log in with previous old password')
        self.SlaveClient.login.insert_username(self.SlaveClient.role.username)
        self.SlaveClient.login.insert_password(self.SlaveClient.role.password)
        self.SlaveClient.login.submit_login()
        assert self.SlaveClient.login.is_already_logged_in(), \
            "client was not able to login with old password -> should be possible"

        logger.info('log out user with old password')
        self.SlaveClient.logout.logout()

        logger.info('initiate password reset with master client')
        self.MasterClient.password_reset.initiate_reset(self.SlaveClient.role.username)

        logger.info('confirm over second factory with slave client')
        self.SlaveClient.password_reset.confirm_over_second_factor()

        logger.info('reset another password with slave client')
        self.SlaveClient.password_reset.change_password(new_password)

        logger.info('make sure that user is not logged in')
        assert not self.SlaveClient.login.is_already_logged_in(), "user is logged in after confirmed password reset"

        logger.info('try to log in with previous old password')
        self.SlaveClient.login.insert_username(self.SlaveClient.role.username)
        self.SlaveClient.login.insert_password(self.SlaveClient.role.password)
        self.SlaveClient.login.submit_login()
        assert not self.SlaveClient.login.is_already_logged_in(), \
            "client was able to login with old password -> should not be possible"

        logger.info('try to log in with new password')
        self.SlaveClient.login.insert_username(self.SlaveClient.role.username)
        self.SlaveClient.login.insert_password(new_password)
        self.SlaveClient.login.submit_login()
        assert self.SlaveClient.login.is_already_logged_in(), \
            "client was unable to login with new password -> should be possible"
