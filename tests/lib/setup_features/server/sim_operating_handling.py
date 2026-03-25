from __future__ import annotations

from balderhub.auth.lib.scenario_features.client.operation_handling_feature import OperationHandlingFeature
from balderhub.auth.lib.utils.operation import Operation
from tests.lib.setup_features.client.dut_manager_feature import DutManagerFeature


class SimOperationHandling(OperationHandlingFeature):
    """Handles operations by delegating to the DUT simulator."""
    dut_sim = DutManagerFeature()

    def enter_operation(self, operation: Operation) -> bool:
        self.dut_sim.dut_simulator.execute_operation(operation)
        return True

    def leave_operation(self, operation: Operation) -> bool:
        return True
