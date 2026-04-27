import balder


class PasswordResetFeature(balder.Feature):
    """
    A feature for managing password reset operations.

    This feature defines the necessary operations for initiating a password
    reset process, handling confirmation through a secondary method or factory,
    and changing the password to a new specified value.

    """
    def initiate_reset(self) -> None:
        """
        Initiates a reset procedure.

        This method should be overridden in subclasses to define the specific
        reset behavior.
        """
        raise NotImplementedError()

    def confirm_over_second_factor(self) -> None:
        """
        Confirms the password-reset operation over a second factor.
        """
        raise NotImplementedError()

    def change_password(self, new_password: str) -> None:
        """
        Changes the password for the current user account, this password-reset was initiated before.

        This method is used to update the current password of the user with a new one.
        The new password must be provided as input and should meet the application's
        password requirements. The implementation of this method should define the
        specific logic for validating and applying the password change.

        :param new_password: The new password to replace the current password.
        """
        raise NotImplementedError()
