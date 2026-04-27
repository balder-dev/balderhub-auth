import balder


class UserLogoutFeature(balder.Feature):
    """
    Feature to logout the user, this feature is assigned to
    """
    def logout(self) -> None:
        """
        logs out the user
        """
        raise NotImplementedError()
