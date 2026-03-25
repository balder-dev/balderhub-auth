from __future__ import annotations

import balder

from balderhub.auth.lib.setup_features.client.authentification_state_machine import AuthenticationStateMachine

from tests.lib.setup_features.client.auth_feature import AuthFeature
from tests.lib.setup_features.client.dut_manager_feature import DutManagerFeature

from tests.lib.setup_features.client.has_perm_for_config import HasPermForConfig
from tests.lib.setup_features.server.auth_for_config import AuthForConfig
from tests.lib.setup_features.server.exist_for_config import ExistForConfig
from tests.lib.setup_features.server.sim_operating_handling import SimOperationHandling


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

class SetupResolvedResources(balder.Setup):
    """A BalderHub setup that tests resolved (normal) Resource objects."""

    class Server(balder.Device):
        existence = ExistForConfig()
        needs_auth_for = AuthForConfig()

    @balder.connect(Server, balder.Connection())
    class Client(balder.Device):
        dut = DutManagerFeature()
        auth = AuthFeature()
        sm_auth = AuthenticationStateMachine()
        operation = SimOperationHandling()
        has_perm_for = HasPermForConfig(Server="Server")


    @balder.fixture('setup')
    def initialize_dut_sim(self):
        self.Client.dut.create()
        yield self.Client.dut
        self.Client.dut.shutdown()
