import balder
from tests.lib.utils import my_action

from tests.lib.utils.dut_simulator import DUTSimulator
from tests.lib.utils.my_resource import MyResource
from tests.lib.utils.my_unresolved_resource import MyUnresolvedResource


class BaseDutManagerFeature(balder.Feature):


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._dut_simulator = None

    @property
    def dut_simulator(self):
        return self._dut_simulator

    def define_dut_environment(self, dut_simulator: DUTSimulator):
        raise NotImplementedError

    def create(self):
        self._dut_simulator = DUTSimulator()
        self.define_dut_environment(self._dut_simulator)

    def shutdown(self):
        self._dut_simulator = None
