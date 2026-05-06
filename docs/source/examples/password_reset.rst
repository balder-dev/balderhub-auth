Password Reset / Forgot Password Workflows
******************************************

This BalderHub package provides scenarios for testing the password reset functionality.

.. note::
    **Testing Websites?** Have a look at the
    `contrib/auth guide at the balderhub-html Documentation <https://hub.balder.dev/projects/html/en/latest/contrib/auth.html>`_.


You can import these scenarios within your environment, like shown below:

.. code-block:: python

    # file `scenario_balderhub_auth.py`

    from balderhub.auth.scenarios import ScenarioPasswordResetWithUnauth, ScenarioPasswordResetWithOtherAuth

Reset: In General
=================

If you want to implement a custom password reset behavior for your special application, you can do that from scratch,
like shown in this chapter. Otherwise, please find below examples from specific domains.

You need to provide a custom implementation of the :class:`balderhub.auth.lib.scenario_features.PasswordResetFeature`:


.. code-block:: python

    class YourCustomPasswordResetFeature(balderhub.auth.lib.scenario_features.PasswordResetFeature):

        def initiate_reset(self) -> None:
            ...

        def confirm_over_second_factor(self) -> None:
            ...

        def change_password(self, new_password: str) -> None:
            ...

Use it for `ScenarioPasswordResetWithUnauth`
--------------------------------------------

If you want to provide an implementation for the :class:`~balderhub.auth.scenarios.ScenarioPasswordResetWithUnauth`, you
can implement a setup like shown below:

Additionally to the previous defined ``YourCustomPasswordResetFeature``, you need to define a user role and a password
provider:


.. code-block:: python

    # file `setups/setup_password_reset.py`

    import balder
    import balderhub.auth.lib.scenario_features.role
    ...

    class ExistingUser(balderhub.auth.lib.scenario_features.role.UserRoleFeature):

        username = 'admin'
        password = 'old-password'

    class NewPasswordProviderFeature(balderhub.auth.lib.scenario_features.PasswordFieldValueProvider):

        def get_valid_new_passwords(self):
            return [
                self.NamedExample(
                    name='Valid Password',
                    value='V#e@r#y1Top2S!e*c(r)et',
                )
            ]

    class SetupExample(balder.Setup):

        class UserDevice(balder.Device):
            user = ExistingUser()
            login = YourImplementationOfUserLoginFeature()
            password_reset = YourCustomPasswordResetFeature()

Use it for `ScenarioPasswordResetWithOtherAuth`
-----------------------------------------------

If you want to trigger the reset by another authenticated user, you can provide a setup implementation for the
:class:`~balderhub.auth.scenarios.ScenarioPasswordResetWithOtherAuth`.

For that, you also need to provide a feature implementation for the
:class:`balderhub.auth.lib.scenario_features.PasswordResetForOtherUserFeature` that holds the implementation to trigger
a password reset for another user.

.. code-block:: python

    class YourCustomPasswordResetForOtherUserFeature(balderhub.auth.lib.scenario_features.PasswordResetForOtherUserFeature):

        def initiate_reset(self, for_user: str):
            ...

Then you can add a setup like shown below. Additionally to the previous defined ``YourCustomPasswordResetFeature`` and
``YourCustomPasswordResetForOtherUserFeature``, you need to define a user role and a password provider here too:

.. code-block:: python

    # file `setups/setup_password_reset.py`

    import balder
    import balderhub.auth.lib.scenario_features.role
    ...

    class ExistingUser(balderhub.auth.lib.scenario_features.role.UserRoleFeature):

        username = 'admin'
        password = 'old-password'

    class NewPasswordProviderFeature(balderhub.auth.lib.scenario_features.PasswordFieldValueProvider):

        def get_valid_new_passwords(self):
            return [
                self.NamedExample(
                    name='Valid Password',
                    value='V#e@r#y1Top2S!e*c(r)et',
                )
            ]

    class SetupExample2(balder.Setup):

        class Server(balder.Device):
            pass

        @balder.connect(Server, balder.Connection())
        class AdminDevice(balder.Device):
            sm_auth = setup_features.client.AuthenticationStateMachine()
            password_reset = YourCustomPasswordResetForOtherUserFeature()

        @balder.connect(Server, balder.Connection())
        class UserDevice(balder.Device):
            user = ExistingUser()
            login = YourImplementationOfUserLoginFeature()
            password_reset = YourCustomPasswordResetFeature()


Reset: For Websites
===================

The ``balderhub-html`` Package provides a ready-to-use implementation for testing the
`registration/password-reset workflows <https://hub.balder.dev/projects/html/en/latest/contrib/auth.html>`_ of website
applications.

It also uses the ``balderhub-smtp`` package to work with confirmation mails - out-of-the box.

For testing a password reset workflow, you can create a setup like shown below:

.. code-block:: python

    import balder
    import balder.connections as cnns

    import balderhub.html.contrib.auth.setup_features
    import balderhub.selenium.lib.setup_features
    import balderhub.smtp.lib.setup_features


    class SetupPasswordReset(balder.Setup):
        class Server(balder.Device):
            pass

        class SmtpServer(balder.Device):
            smtp = balderhub.smtp.lib.setup_features.AiosmtpdServerFeature()

        @balder.connect(SmtpServer, over_connection=cnns.SmtpConnection)
        @balder.connect(Server, over_connection=balder.Connection)
        class Client(balder.Device):
            selenium = balderhub.selenium.lib.setup_features.SeleniumXXWebdriverFeature()  # or other feature that supports `balderhub-webdriver`

            role = MyUserRole()

            page_login = LoginPage()
            login = balderhub.html.contrib.auth.setup_features.UserLoginFeature()

            page_req_passwd_reset = PasswordResetRequestPage()
            page_finalize_passwd_reset = PasswordResetFinalizationPage()
            page_passwd_reset_confirm = PasswordResetConfirmationPage()

            passwd_reset = balderhub.html.contrib.auth.setup_features.PasswordResetFeature()

            mail = balderhub.smtp.lib.setup_features.ProxySmtpReader(SmtpServer='SmtpServer')
            mail_confirm = MailConfirmationForPasswdResetByXXFeature()

Please refer to the ``contrib/auth`` section of the ``balderhub-html`` documentation for further details and the
different ready-implemented workflows
(`Link to Documentation <https://hub.balder.dev/projects/html/en/latest/contrib/auth.html>`_).
