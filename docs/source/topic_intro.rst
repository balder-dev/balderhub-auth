Introduction into Auth
**********************

The ``balderhub-auth`` package is a specialized BalderHub collection designed to simplify and standardize the testing
of authentication and authorization systems. It provides a comprehensive set of predefined Features and Scenarios that
can be easily integrated into your Balder projects.

Authentication Methods
======================

The ``balderhub-auth`` package supports different methods for authenticating a device or user. These are primarily
managed through "Role" features:

* **User/Password Authentication**: Represented by ``UserRoleFeature``, this method uses a standard username and
  password combination to establish identity.
* **Token Authentication**: Represented by ``TokenRoleFeature``, this method uses a security token (like a Bearer token
  or API key) for authentication (no scenarios implemented yet).

Authentication Features/Workflows
---------------------------------

The ``balderhub-auth`` package provides several features to manage and test the authentication state of a device:

* **Authentication State Machine**: Managed via the ``AuthenticationStateMachine`` feature, it tracks whether a device
  is currently in an ``AUTHENTICATED`` or ``UNAUTHENTICATED`` state.
* **Login and Logout**: The ``UserLoginFeature`` and ``UserLogoutFeature`` provide the necessary actions (like entering
  credentials and submitting) to perform transitions between authentication states.
* **Registration**: The ``RegisterSelfFeature`` allows testing the workflow where a new user account is created.
* **Password Management**: Features like ``PasswordResetFeature`` and ``PasswordResetForOtherUserFeature`` handle the
  multi-step process of resetting credentials, including second-factor confirmation.

Provided Authentication Scenarios
---------------------------------

The package includes ready-to-use scenarios for common identity management tasks:

* **Simple Login**: The ``ScenarioSimpleLogin`` verifies that a user can successfully authenticate using valid
  credentials and that the device state correctly transitions to authenticated.
* **New User Registration**: The ``ScenarioRegisterNewAsUnauth`` tests the entire flow of an unauthenticated client
  registering a new account and then successfully logging in with the new credentials.
* **Self-Service Reset**: The ``ScenarioPasswordResetWithUnauth`` handles the "forgot password" case, where an
  unauthenticated user initiates a reset, confirms it via a second factor, and sets a new password.
* **Coordinated Reset**: The ``ScenarioPasswordResetWithOtherAuth`` tests a more complex workflow where one
  authenticated device initiates a password reset for another user (e.g., an administrative reset).

What are Permissions?
=====================

In the context of ``balderhub-auth``, **permissions** define the access rights a user or device has to specific
resources. Permissions determine whether an operation (like reading, creating, or deleting) is allowed for a given
identity. The package distinguishes between general permissions and object-level permissions, allowing you to test
complex access control logic where access might depend on the specific instance of a resource.

The package uses specific "ForConfig" features to define the expected state and rules of the System Under Test (SUT).
These features are typically implemented on the server-side (to define rules) or client-side (to define capabilities).

ExistenceForConfig
------------------

This feature represents the **existence rule configuration** for a server device. It is used to define which resources
currently exist in the system and which do not. This is crucial for testing scenarios where the outcome depends on the
presence of a resource (e.g., trying to access a non-existent object should return a 404 error regardless of
permissions).

AuthenticationForConfig
-----------------------

This feature represents the **authentication rule configuration** for a server device. It defines which resources
require authentication and which are publicly accessible. By providing lists of resources that require (or do not
require) authentication, it allows the scenarios to automatically verify if the SUT correctly enforces authentication
boundaries.

HasPermissionsForConfig
-----------------------

This feature represents the **permission rule configuration** for a client/user device. It defines which permissions
the current user is supposed to have. Scenarios use this information to verify that the user can indeed perform
permitted operations and is blocked from forbidden ones.

Coming Soon
===========

This package is still under development.

New scenarios for edge-cases, wrong field content and admin user management will be added soon.

If you would like to contribute, feel free to
`create new pull requests <https://github.com/balder-dev/balderhub-auth/pulls>`_.