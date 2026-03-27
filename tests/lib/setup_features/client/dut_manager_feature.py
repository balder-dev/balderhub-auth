from tests.lib.scenario_features.base_dut_manager_feature import BaseDutManagerFeature
from tests.lib.utils import my_action
from tests.lib.utils.dut_simulator import DUTSimulator

from tests.lib.utils.my_resource import MyResource
from tests.lib.utils.my_unresolved_resource import MyUnresolvedResource


class DutManagerFeature(BaseDutManagerFeature):


    def define_dut_environment(self, dut_simulator: DUTSimulator):
        dut_simulator.add_public_resource(MyResource('public'), actions=[my_action.RETRIEVE])

        dut_simulator.add_authenticated_resource(MyResource('articles'), actions=[my_action.RETRIEVE, my_action.CREATE, my_action.DELETE])
        dut_simulator.add_authenticated_resource(MyResource('users'), actions=[my_action.RETRIEVE, my_action.CREATE])

        dut_simulator.grant_permission('testuser', MyResource('articles'), my_action.CREATE)
        dut_simulator.grant_permission('testuser', MyResource('articles'), my_action.RETRIEVE)
        dut_simulator.grant_permission('testuser', MyResource('users'), my_action.RETRIEVE)

        # unresolved resources (object-level permissions)
        # items 1, 2, 3 exist as resolved instances of 'items'
        for item_id in [1, 2, 3]:
            resolved = MyUnresolvedResource('items').get_resolved_resource(MyUnresolvedResource.Parameter(item_id))
            dut_simulator.add_authenticated_resource(resolved, actions=[my_action.RETRIEVE, my_action.UPDATE, my_action.DELETE])

        # testuser has permission for items 1 and 2 (RETRIEVE, UPDATE) but not item 3
        for item_id in [1, 2]:
            resolved = MyUnresolvedResource('items').get_resolved_resource(MyUnresolvedResource.Parameter(item_id))
            dut_simulator.grant_permission('testuser', resolved, my_action.RETRIEVE)
            dut_simulator.grant_permission('testuser', resolved, my_action.UPDATE)
