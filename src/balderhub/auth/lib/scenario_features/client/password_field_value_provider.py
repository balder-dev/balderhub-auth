from typing import Optional
import dataclasses

import balder


class PasswordFieldValueProvider(balder.Feature):
    """
    Provides various password examples to test password field functionality.

    This class is designed to supply password examples, both valid and invalid, to facilitate exhaustive testing of
    password field validation.
    """
    @dataclasses.dataclass
    class NamedExample:
        """
        A data structure representing a password example.
        It includes a name for the example, the password value, and an optional expected error message for invalid cases
        """
        name: str
        value: str
        expected_error_message: Optional[str] = None

    def get_primary_valid_password(self) -> NamedExample:
        """
        Retrieve the primary valid password for a given entity.

        This method is used by test scenarios that just want a valid password. The default implementation returns the
        first valid example provided by
        :meth:`balderhub.auth.lib.scenario_features.client.PasswordFieldValueProvider.get_valid_new_passwords`.

        :return: The primary valid password example dataclasss.
        """
        return self.get_valid_new_passwords()[0]

    def get_valid_new_passwords(self) -> list[NamedExample]:
        """
        Retrieves a list of valid new password suggestions.

        This method is expected to return a collection of password examples that are
        considered valid based on certain criteria.

        :return: A list of NamedExample objects representing valid password suggestions
        """
        raise NotImplementedError()

    def get_invalid_passwords(self) -> list[NamedExample]:
        """
        Retrieves a list of invalid password examples.

        This method is intended to be implemented in derived classes to return
        a list of passwords that are considered invalid based on specific
        validation criteria.

        :return: A list of invalid password examples
        """
        raise NotImplementedError()
