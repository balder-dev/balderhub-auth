import logging
import balder
from ..lib import scenario_features

logger = logging.getLogger(__file__)


class ScenarioPasswordResetWithUnauth(balder.Scenario):
    """
    This class defines a scenario for testing password reset functionality with an unauthenticated client. It ensures
    that the password reset process works as intended and validates that the user cannot log in with the old password
    after the reset, but can log in with the new password.
    """

    class UnauthClient(balder.Device):
        """he unauthenticated client device used for performing the password-reset."""
        #: user role describing username and password
        role = scenario_features.client.role.UserRoleFeature()
        #: login feature allowing to perform the login process
        login = scenario_features.client.UserLoginFeature()
        #: provider for password field values
        passwd_provider = scenario_features.client.PasswordFieldValueProvider()
        #: feature for resetting the password
        password_reset = scenario_features.client.PasswordResetFeature()

    def test_password_reset(self):
        """
        Tests the password reset functionality by ensuring that a user can reset their password
        successfully, and the old password becomes invalid while the new password permits access.
        """
        new_password = self.UnauthClient.passwd_provider.get_primary_valid_password().value

        logger.info('initiate password reset')
        self.UnauthClient.password_reset.initiate_reset()

        logger.info('confirm over second factory')
        self.UnauthClient.password_reset.confirm_over_second_factor()

        logger.info('reset another password')
        self.UnauthClient.password_reset.change_password(new_password)

        logger.info('make sure that user is not logged in')
        assert not self.UnauthClient.login.is_already_logged_in(), "user is logged in after confirmed password reset"

        logger.info('try to log in with previous old password')
        self.UnauthClient.login.insert_username(self.UnauthClient.role.username)
        self.UnauthClient.login.insert_password(self.UnauthClient.role.password)
        self.UnauthClient.login.submit_login()
        assert not self.UnauthClient.login.is_already_logged_in(), \
            "client was able to login with old password -> should not be possible"

        logger.info('try to log in with new password')
        self.UnauthClient.login.insert_username(self.UnauthClient.role.username)
        self.UnauthClient.login.insert_password(new_password)
        self.UnauthClient.login.submit_login()
        assert self.UnauthClient.login.is_already_logged_in(), \
            "client was unable to login with new password -> should be possible"
