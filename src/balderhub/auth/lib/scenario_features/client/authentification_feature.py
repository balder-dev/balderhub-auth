import balder


class AuthenticationFeature(balder.Feature):
    """
    This is the base feature class to authenticate the user device.
    """

    @property
    def is_authenticated(self) -> bool:
        """returns True if the user is authenticated, False otherwise"""
        raise NotImplementedError()

    def authenticate(self):
        """authenticates the user"""
        raise NotImplementedError

    def unauthenticate(self):
        """unauthenticates the user"""
        raise NotImplementedError
