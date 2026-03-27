import balderhub.auth.lib.scenario_features.client
from tests.lib.scenario_features.base_dut_manager_feature import BaseDutManagerFeature


class AuthFeature(balderhub.auth.lib.scenario_features.client.AuthenticationFeature):
    """Simple authentication feature backed by a boolean flag."""
    USERNAME = 'testuser'

    dut_sim = BaseDutManagerFeature()

    @property
    def is_authenticated(self) -> bool:
        return self.dut_sim.dut_simulator.authenticated_username == self.USERNAME

    def authenticate(self):
        self.dut_sim.dut_simulator.authenticate(self.USERNAME)

    def unauthenticate(self):
        self.dut_sim.dut_simulator.unauthenticate()
