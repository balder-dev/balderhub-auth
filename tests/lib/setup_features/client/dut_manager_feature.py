import balder
from tests.lib.utils import my_action

from tests.lib.utils.dut_simulator import DUTSimulator
from tests.lib.utils.my_resource import MyResource


class DutManagerFeature(balder.Feature):


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._dut_simulator = None



    @property
    def dut_simulator(self):
        return self._dut_simulator


    def create(self):
        self._dut_simulator = DUTSimulator()
        self._dut_simulator.add_public_resource(MyResource('public'), actions=[my_action.RETRIEVE])

        self._dut_simulator.add_authenticated_resource(MyResource('articles'), actions=[my_action.RETRIEVE, my_action.CREATE, my_action.DELETE])
        self._dut_simulator.add_authenticated_resource(MyResource('users'), actions=[my_action.RETRIEVE, my_action.CREATE])

        self._dut_simulator.grant_permission('testuser', MyResource('articles'), my_action.CREATE)
        self._dut_simulator.grant_permission('testuser', MyResource('articles'), my_action.RETRIEVE)
        self._dut_simulator.grant_permission('testuser', MyResource('users'), my_action.RETRIEVE)

    def shutdown(self):
        self._dut_simulator = None
