Registration
************

This BalderHub package provides an simple scenario for registering a new unauthenticated user.

.. note::
    **Testing Websites?** Have a look at the
    `contrib/auth guide at the balderhub-html Documentation <https://hub.balder.dev/projects/html/en/latest/contrib/auth.html>`_.


You can import this scenario within your environment, like shown below:

.. code-block:: python

    # file `scenario_balderhub_auth.py`

    from balderhub.auth.scenarios import ScenarioRegisterNewAsUnauth

Registration: In General
========================

If you want to implement a custom registration behavior for your special application, you can do that from scratch, like
shown in this chapter. Otherwise, please find below examples from specific domains.

In addition to the need to implement the login feature (see :ref:`Login\: In General`), you also need to provide a
custom implementation of the :class:`balderhub.auth.lib.scenario_features.RegisterSelfFeature`:


.. code-block:: python

    class YourCustomRegisterSelfFeature(balderhub.auth.lib.scenario_features.RegisterSelfFeature):

        def register(self):
            ...


You can use it, by importing both of them into your setup and defining a user role, that should be used for
the new user that is created with this registration:


.. code-block:: python

    # file `setups/setup_registration.py`

    import balder
    import balderhub.auth.lib.scenario_features.role
    ...

    class NotExistingUser(balderhub.auth.lib.scenario_features.role.UserRoleFeature):

        username = 'temp'
        password = 'very-top-secret'

    class SetupExample(balder.Setup):

        class NewUser(balder.Device):
            user = NotExistingUser()
            login = YourImplementationOfUserLoginFeature()
            register = YourCustomRegisterSelfFeature()


Registration: For Websites
==========================

The ``balderhub-html`` Package provides a ready-to-use implementation for testing the
`registration/password-reset workflows <https://hub.balder.dev/projects/html/en/latest/contrib/auth.html>`_ of website
applications.

It also uses the ``balderhub-smtp`` package to work with confirmation mails - out-of-the box.

For testing an all-in-one registration workflow, you can create a setup like shown below:

.. code-block:: python

    import balder
    import balder.connections as cnns

    import balderhub.html.contrib.auth.setup_features
    import balderhub.selenium.lib.setup_features
    import balderhub.smtp.lib.setup_features


    class SetupAllInOneRegistration(balder.Setup):
        class Server(balder.Device):
            pass

        class SmtpServer(balder.Device):
            smtp = balderhub.smtp.lib.setup_features.AiosmtpdServerFeature()

        @balder.connect(SmtpServer, over_connection=cnns.SmtpConnection)
        @balder.connect(Server, over_connection=balder.Connection)
        class UnregisteredClient(balder.Device):
            selenium = balderhub.selenium.lib.setup_features.SeleniumXXWebdriverFeature()  # or other feature that supports `balderhub-webdriver`

            role = UnregisteredUserRole()

            page_login = LoginPage()
            login = balderhub.html.contrib.auth.setup_features.UserLoginFeature()

            page_register = RegistrationAllInOnePage()
            page_registration_confirm = RegistrationConfirmationPage()

            registration = balderhub.html.contrib.auth.setup_features.RegisterSelfAllDataAtOnceFeature()

            mail = balderhub.smtp.lib.setup_features.ProxySmtpReader(SmtpServer='SmtpServer')
            mail_confirm = MailConfirmationForRegistrationByXXFeature()

You only need to provide the selectors for your webpages and an the implementation of the
``MailConfirmationForRegistrationByXXFeature``, that extracts the link/token from the mail body and you're ready to go.

Please refer to the ``contrib/auth`` section of the ``balderhub-html`` documentation for further details and the
different ready-implemented workflows
(`Link to Documentation <https://hub.balder.dev/projects/html/en/latest/contrib/auth.html>`_).