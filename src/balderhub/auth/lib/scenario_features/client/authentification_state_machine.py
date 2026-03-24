import enum

import balder

class StateMachine(balder.Feature):
    """
    This is the base class for all state machine features.
    """
    # TODO this feature needs to be moved to main balder project

    class State(enum.Enum):
        """
        Base class for all states.
        """

    class ImpossibleStateChangeError(Exception):
        """
        Exception that is raised if a state change is not possible.
        """

    @property
    def current_state(self):
        """returns the current state of the state machine"""
        raise NotImplementedError()

    def assert_expected_state(self, state: State):
        """
        Asserts that the current state is the expected state.

        :param state: the expected state
        """
        assert self.current_state == state, f"expected state `{state}`, got state `{self.current_state}`"

    def change_state_to(self, state: State):
        """
        Changes the current state to the given state.

        :param state: the state to change to
        """
        raise NotImplementedError()


class AuthenticationStateMachine(StateMachine):
    """
    This is the feature class representing an authentication state machine.
    """

    class State(StateMachine.State):
        """
        The states for the authentication state machine.
        """
        AUTHENTICATED = 'authenticated'
        UNAUTHENTICATED = 'unauthenticated'

    @property
    def current_state(self):
        """returns the current state of the authentication state machine"""
        raise NotImplementedError()

    def change_state_to(self, state: State):
        """
        Changes the current state of the authentication state machine to the given state.

        :param state: the state to change to
        """
        raise NotImplementedError()
