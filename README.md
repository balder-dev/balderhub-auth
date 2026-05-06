# BalderHub Package ``balderhub-auth``

This is a BalderHub package for the [Balder](https://docs.balder.dev) test framework. It provides different features and scenarios 
for testing authentification and authorization (permissions, login, ...).

If you are new to Balder check out the [official documentation](https://docs.balder.dev) first.

The ``balderhub-auth`` package is a specialized BalderHub collection designed to simplify and standardize the testing
of authentication and authorization systems. It provides a comprehensive set of predefined Features and Scenarios that
can be easily integrated into your Balder projects.

This package covers several core areas of identity and access management:

* **Authentication Workflows**: Includes ready-to-use scenarios for user login, registration, and logout processes.
* **Account Management**: Provides scenarios for password reset workflows, both for unauthenticated users and those
  already logged in.
* **Permission & Authorization**: Test Scenarios for testing both general permissions and specific
  object-level permissions, ensuring that access control logic is correctly implemented.
* **State Management**: Includes an authentication state machine to handle transitions between different
  authentication states during test execution.

If you want to write **tests for web application** also have a look into 
[the contrib section of ``balderhub-html``](https://hub.balder.dev/projects/html/en/latest/contrib/auth.html) for 
ready-to-use implementation of these test scenarios.

## Installation

You can install the latest release with pip:

```
python -m pip install balderhub-auth
```

# Check out the documentation

If you need more information, 
[checkout the ``balderhub-auth`` documentation](https://hub.balder.dev/projects/auth).


# License

This BalderHub package is free and Open-Source

Copyright (c)  2025  balderhub-auth

Distributed under the terms of the MIT license