Scenarios
*********

Scenarios describe **what you need**. They define the tests and the necessary devices for them. Here you can find all
scenarios that are implemented in this BalderHub package.

Login Scenarios
===============

.. autoclass:: balderhub.auth.scenarios.ScenarioSimpleLogin
    :members:


Registration Scenarios
======================

.. autoclass:: balderhub.auth.scenarios.ScenarioRegisterNewAsUnauth
    :members:

Password-Reset Scenarios
========================

.. autoclass:: balderhub.auth.scenarios.ScenarioPasswordResetWithUnauth
    :members:

.. autoclass:: balderhub.auth.scenarios.ScenarioPasswordResetWithOtherAuth
    :members:

Permission Test Scenarios
=========================

Permission Scenarios
--------------------

.. autoclass:: balderhub.auth.scenarios.ScenarioAuthpermAuthenticated
    :members:

.. autoclass:: balderhub.auth.scenarios.ScenarioAuthpermUnauthenticated
    :members:

Object-Permission Specific Scenarios
------------------------------------

.. autoclass:: balderhub.auth.scenarios.ScenarioAuthpermAuthenticatedObjperm
    :members:

.. autoclass:: balderhub.auth.scenarios.ScenarioAuthpermUnauthenticatedObjperm
    :members:

Abstract Helper Scenarios for Permissions
-----------------------------------------

.. autoclass:: balderhub.auth.scenarios.abstract_scenario_authperm_authenticated.AbstractScenarioAuthpermAuthenticated
    :members:

.. autoclass:: balderhub.auth.scenarios.abstract_scenario_authperm_unauthenticated.AbstractScenarioAuthpermUnauthenticated
    :members:
