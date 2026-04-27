import balder


class PasswordResetForOtherUserFeature(balder.Feature):
    """
    Handles the functionality for initiating a password reset for another user.

    This feature defines the interface or behavior allowing the initiation of a
    password reset process for a specified user, that is not the user that triggers this request.
    """

    def initiate_reset(self, for_user: str) -> None:
        """
        Initiates a reset process for the specified user.

        This method serves as a placeholder for implementing the reset logic
        for a given user.

        :param for_user: The user for whom the reset process is to be initiated.
        """
        raise NotImplementedError()
