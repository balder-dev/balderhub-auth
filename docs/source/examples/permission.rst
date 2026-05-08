Permissions
***********

This Package provides different scenarios and features for testing authentification and permission requiring resources.

.. note::
    This section covers the raw implementation of authentification and permission access tests. If your
    application-under-test is a web application, have a look into the contrib section of the balderhub-http and
    balderhub-webdriver project. These packages already provide a ready-to-use implementation for validating your web
    endpoints.

    If you already use an implementation of the
    :class:`balderhub.http.lib.scenario_features.client.WebSessionFeature` feature (from
    `balderhub-http Package <https://hub.balder.dev/projects/http>`_)
    or the :class:`balderhub.webdriver.lib.scenario_features.WebdriverControlFeature` (from
    `balderhub-webdriver Package <https://hub.balder.dev/projects/webdriver>`_, that is implemented by
    :class:`balderhub.selenium.lib.scenario_features.SeleniumFeature`) you normally do not have to define more
    than the urls to test. The BalderHub packages will care about everything else.

    More information are available within the
    `contrib section of the balderhub-http package documentation <https://hub.balder.dev/projects/http/en/latest/contrib.html>`_ or the
    `contrib section of the balderhub-webdriver package documentation <https://hub.balder.dev/projects/webdriver/en/latest/contrib.html>`_.

Permission Tests Introduction
=============================



Main Configuration Features
---------------------------

There are three main features that allows to define the access rights of your system:

+-------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| Device Type | Feature                                                                        | Description                                                             |
+=============+================================================================================+=========================================================================+
| **Server**  | :class:`~balderhub.auth.lib.scenario_features.server.ExistenceForConfig`       | Provides all :class:`~balderhub.auth.lib.utils.ResourceRule` objects    |
|             |                                                                                | (describes the resource with the applied action) that exists and all    |
|             |                                                                                | that does not exist, but should explicitly be validated with these      |
|             |                                                                                | scenarios                                                               |
+-------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| **Server**  | :class:`~balderhub.auth.lib.scenario_features.server.AuthenticationForConfig`  | Provides all :class:`~balderhub.auth.lib.utils.ResourceRule` objects    |
|             |                                                                                | that needs an authenticated user in general and all that are            |
|             |                                                                                | accessible for unauthenticated users too                                |
+-------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| **Client**  | :class:`~balderhub.auth.lib.scenario_features.server.HasPermissionsForConfig`  | Provides all :class:`~balderhub.auth.lib.utils.ResourceRule` objects    |
|             |                                                                                | this user device has permission for and also all the resource, this     |
|             |                                                                                | specific user does not have permissions for                             |
+-------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------+
| **Client**  | :class:`~balderhub.auth.lib.scenario_features.server.IsUnauthenticatedFeature` | Autonomous feature specifying that the device is an unauth device       |
+-------------+--------------------------------------------------------------------------------+-------------------------------------------------------------------------+

Within these features a list of resouce roules need to be configured, that describes the expected behaviour.

You can use the normal :class:`~balderhub.auth.lib.utils.ResourceRule`, but you can also use your custom implementation
of the :class:`~balderhub.auth.lib.utils.UnresolvedResource`, for defining unresolved resources, mostly used for
defining specific data-item related endpoints. The latter also allows you to check individual object permissions, f.e.
for data-item related tests.

Defining Resources and Rules
----------------------------

If you have different user roles, you can add them by creating multiple client devices connected to the server instance.

For example, a setup for testing permissions could look like shown below:

.. code-block:: python

    import balder

    class SetupExample(balder.Setup):

        class Server(balder.Device):
            exists = MyExistenceForConfig()
            auth_for = MyAuthenticationForConfig()

        @balder.connect(Server, over_connection=balder.Connection)
        class AdminUser(balder.Device):
            perm = AdminHasPermissionsForConfig()
            ...

        @balder.connect(Server, over_connection=balder.Connection)
        class NormalUser(balder.Device):
            perm = NormalUserHasPermissionsForConfig()
            ...

        @balder.connect(Server, over_connection=balder.Connection)
        class UnauthUser(balder.Device):
            _unauth = IsUnauthenticatedFeature()
            ...

Implementing the ``OperationHandlingFeature``
---------------------------------------------

All permission scenarios needs an implementation of the
:class:`~balderhub.auth.lib.scenario_features.client.OperationHandlingFeature`. Find an example implementation below:

.. code-block:: python

    ...
    from balderhub.auth.lib.scenario_features.client import OperationHandlingFeature


    class MyImplementationOfOperationHandlingFeature(OperationHandlingFeature):

        def enter_operation(self, operation: Operation) -> bool:
            ..  # TODO develop process to enter an operation (resource over an specific Action)
            return True

        def leave_operation(self, operation: Operation) -> bool:
            ..  # TODO develop process to leave an operation (resource over an specific Action) - f.e. clean up
            return True


.. note::
    If you're testing a web application, you can use the ready-to-use implementation of this feature within the
    ``balderhub-http`` or the ``balderhub-webdriver`` (mostly used with selenium):

    * :class:`balderhub.http.contrib.auth.setup_features.client.OperationHandlingOverWebsessionFeature`: Can be used
      for testing web end points specially REST endpoints (uses the ``requests`` package as base)
    * :class:`balderhub.webdriver.contrib.auth.setup_features.client.OperationHandlingOverWebdriverFeature`: Can be used
      for testing graphical web interfaces, specially if you already use selenium or other webdriver supported balderhub
      packages

Providing your own UnresolvedResource type
------------------------------------------

This package has been implemented in a very versatile way. The main resource type, that is used, when testing object
permission is the :class:`~balderhub.auth.lib.utils.UnresolvedResource`. This is an abstract class that need to be
overwritten, before it can be used:

.. code-block:: python

    from balderhub.auth.lib.utils.unresolved_resource import UnresolvedResource
    from balderhub.auth.lib.utils.resource import Resource
    from tests.lib.utils.my_resource import MyResource


    class UserAccountResource(UnresolvedResource):

        class Parameter(UnresolvedResource.Parameter):
            def __init__(self, username: str):
                self.username = username

            def __eq__(self, other):
                return isinstance(other, UserAccountResource.Parameter) and self.username == other.username

            def __hash__(self):
                return hash(self.username)

        def __eq__(self, other):
            return isinstance(other, MyUnresolvedResource) and self.name == other.name

        def __hash__(self):
            return hash(self.name)

        def get_resolved_resource(self, param: 'UserAccountResource.Parameter') -> Resource:
            return MyResource(f'/home/{param.username}')


It is important to implement the :meth:`~balderhub.auth.lib.utils.UnresolvedResource.get_resolved_resource`, because this
method resolves the unresolved resource into an resolved one.

.. note::
    If your parameters are specified by data-items from the
    `balderhub-data package <https://hub.balder.dev/projects/data>`_ you can use the already implemented
    unresolved-resource :class:`balderhub.data.contrib.auth.utils.ResourceForSpecificDataItem`.

    The package also provides an implementation of the
    :class:`~balderhub.auth.lib.scenario_features.client.UnresolvedResourceParameterConfig` described below. You can
    use the factory :class:`balderhub.data.contrib.auth.setup_features.factories.AutoDataParamProviderFactory` or
    implementing your own version by overwriting the
    :class:`balderhub.data.contrib.auth.setup_features.DataItemParamProvider` directly.

Additionally to the normal features, that are used for the normal scenarios, the object-permission test scenarios also
need an implementation of the :class:`~balderhub.auth.lib.scenario_features.client.UnresolvedResourceParameterConfig`.
This feature defines which object-variants are verified within the test:

.. code-block:: python

    from balderhub.auth.lib.scenario_features.client.unresolved_resource_parameter_config import UnresolvedResourceParameterConfig
    from balderhub.auth.lib.utils.unresolved_resource import UnresolvedResource
    from tests.lib.utils.my_unresolved_resource import MyUnresolvedResource


    class UnresolvedParamConfig(UnresolvedResourceParameterConfig):
        """Provides parameters for unresolved resources used in tests."""

        def get_parameters_for(self, resource_rule) -> list[UnresolvedResource.Parameter]:
            if isinstance(resource_rule.resource, UserAccountResource):
                return [
                    UserAccountResource.Parameter('admin'),
                    UserAccountResource.Parameter('guest'),
                    UserAccountResource.Parameter('developer'),
                ]
            else:
                raise NotImplementedError()


Testing Non-Object-Permissions
==============================

This BalderHub project provides two different scenarios for testing resolved resources (defined by normal
:class:`~balderhub.auth.lib.utils.ResourceRule`).

The :class:`~balderhub.auth.scenarios.ScenarioAuthpermUnauthenticated`:

.. image:: /_static/ScenarioAuthpermUnauthenticated.svg
    :align: center
    :alt: Visual Description of this ``ScenarioAuthpermUnauthenticated``

The following code shows an example setup that runs the
:class:`~balderhub.auth.scenarios.ScenarioAuthpermUnauthenticated`:

.. code-block:: python

    import balder

    class SetupExample(balder.Setup):

        class Server(balder.Device):
            exists = MyExistenceForConfig()
            auth_for = MyAuthenticationForConfig()

        @balder.connect(Server, over_connection=balder.Connection)
        class UnauthUser(balder.Device):
            _is_unauth = balderhub.auth.lib.scenario_features.server.IsUnauthenticatedFeature()
            operation = MyImplementationOfOperationHandlingFeature()


The :class:`~balderhub.auth.scenarios.ScenarioAuthpermAuthenticated`:

.. image:: /_static/ScenarioAuthpermAuthenticated.svg
    :align: center
    :alt: Visual Description of this ``ScenarioAuthpermAuthenticated``

The following code shows an example setup that runs the
:class:`~balderhub.auth.scenarios.ScenarioAuthpermAuthenticated`:

.. code-block:: python

    import balder

    class SetupExample(balder.Setup):

        class Server(balder.Device):
            exists = MyExistenceForConfig()
            auth_for = MyAuthenticationForConfig()

        @balder.connect(Server, over_connection=balder.Connection)
        class AdminUser(balder.Device):
            operation = MyImplementationOfOperationHandlingFeature()
            perm = AdminHasPermissionsForConfig()


Testing Object-Permissions
==========================

Similar to the previous scenarios, there is also a dedicated scenario for each one that explicitly tests object
permissions by using the :class:`~balderhub.auth.lib.utils.UnresolvedResource`. These resources allow you to define
programmatic rules to specify the conditions that must apply to an element for the user to have permission or for
authentication to be required.

The :class:`~balderhub.auth.scenarios.ScenarioAuthpermUnauthenticatedObjperm`:

.. image:: /_static/ScenarioAuthpermUnauthenticatedObjperm.svg
    :align: center
    :alt: Visual Description of this ``ScenarioAuthpermUnauthenticatedObjperm``

The following code shows an example setup that runs the
:class:`~balderhub.auth.scenarios.ScenarioAuthpermUnauthenticatedObjperm`:

.. code-block:: python

    import balder

    class SetupExample(balder.Setup):

        class Server(balder.Device):
            exists = MyExistenceForConfig()
            auth_for = MyAuthenticationForConfig()

        @balder.connect(Server, over_connection=balder.Connection)
        class UnauthUser(balder.Device):
            _is_unauth = balderhub.auth.lib.scenario_features.server.IsUnauthenticatedFeature()
            operation = MyImplementationOfOperationHandlingFeature()


The :class:`~balderhub.auth.scenarios.ScenarioAuthpermAuthenticatedObjperm`:

.. image:: /_static/ScenarioAuthpermAuthenticatedObjperm.svg
    :align: center
    :alt: Visual Description of this ``ScenarioAuthpermAuthenticatedObjperm``

The following code shows an example setup that runs the
:class:`~balderhub.auth.scenarios.ScenarioAuthpermAuthenticatedObjperm`:

.. code-block:: python

    import balder

    class SetupExample(balder.Setup):

        class Server(balder.Device):
            exists = MyExistenceForConfig()
            auth_for = MyAuthenticationForConfig()

        @balder.connect(Server, over_connection=balder.Connection)
        class AdminUser(balder.Device):
            operation = MyImplementationOfOperationHandlingFeature()
            perm = AdminHasPermissionsForConfig()
