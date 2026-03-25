import balderhub.auth.lib.scenario_features.client
from tests.lib.setup_features.client.dut_manager_feature import DutManagerFeature


class AuthFeature(balderhub.auth.lib.scenario_features.client.AuthenticationFeature):
    """Simple authentication feature backed by a boolean flag."""
    USERNAME = 'testuser'

    dut_sim = DutManagerFeature()

    @property
    def is_authenticated(self) -> bool:
        return self.dut_sim.dut_simulator.authenticated_username == self.USERNAME

    def authenticate(self):
        self.dut_sim.dut_simulator.authenticate(self.USERNAME)

    def unauthenticate(self):
        self.dut_sim.dut_simulator.unauthenticate()
