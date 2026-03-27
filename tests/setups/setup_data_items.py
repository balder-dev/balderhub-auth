from __future__ import annotations
import balder
from balderhub.auth.lib.setup_features.client.authentification_state_machine import AuthenticationStateMachine
from tests.lib.setup_features.client.auth_feature import AuthFeature
from tests.lib.setup_features.client.data_item_dut_manager_feature import DataItemDutManagerFeature
from tests.lib.setup_features.client.data_item_has_perm_for_config import DataItemHasPermForConfig
from tests.lib.setup_features.client.data_item_unresolved_param_config import DataItemUnresolvedParamConfig
from tests.lib.setup_features.server.data_item_auth_for_config import DataItemAuthForConfig
from tests.lib.setup_features.server.data_item_exist_for_config import DataItemExistForConfig
from tests.lib.setup_features.server.sim_operating_handling import SimOperationHandling


class SetupDataItems(balder.Setup):
    """A BalderHub setup that tests unresolved (object-level) Resource objects."""

    class Server(balder.Device):
        existence = DataItemExistForConfig()
        needs_auth_for = DataItemAuthForConfig()

    @balder.connect(Server, balder.Connection())
    class Client(balder.Device):
        dut = DataItemDutManagerFeature()
        auth = AuthFeature()
        sm_auth = AuthenticationStateMachine()
        operation = SimOperationHandling()
        has_perm_for = DataItemHasPermForConfig(Server="Server")
        param_provider = DataItemUnresolvedParamConfig()

    @balder.fixture('setup')
    def initialize_dut_sim(self):
        self.Client.dut.create()
        yield self.Client.dut
        self.Client.dut.shutdown()
