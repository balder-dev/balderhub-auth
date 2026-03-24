from balderhub.auth.lib import scenario_features


class AuthenticationStateMachine(scenario_features.client.AuthenticationStateMachine):
    """
    Manages and transitions between authentication states.

    The AuthenticationStateMachine class serves as a high-level abstraction for handling authentication states such as
    authenticated and unauthenticated. It ensures state transitions are valid and performs the necessary actions to
    switch between states.

    It provides a setup-level implementation of
    :class:`balderhub.auth.lib.scenario_features.client.AuthenticationStateMachine`.
    """
    auth = scenario_features.client.authentification_feature.AuthenticationFeature()

    @property
    def current_state(self):
        return self.State.AUTHENTICATED if self.auth.is_authenticated else self.State.UNAUTHENTICATED

    def change_state_to(
            self,
            state: scenario_features.client.authentification_state_machine.AuthenticationStateMachine.State
    ):
        if state == self.State.AUTHENTICATED and self.current_state == self.State.UNAUTHENTICATED:
            self.auth.authenticate()
            return
        if state == self.State.UNAUTHENTICATED and self.current_state == self.State.AUTHENTICATED:
            self.auth.unauthenticate()
            return
        raise self.ImpossibleStateChangeError(f'can not change state from {self.current_state} to {state}')
