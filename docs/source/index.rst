BalderHub Auth
==============


.. note::
    Please note, this package is still under development. If you would like to contribute, take a look into the
    `project <https://github.com/balder-dev/balderhub-auth/>`_.


This is a BalderHub package for the `Balder <https://docs.balder.dev/>`_ test framework. If you are new to Balder check
out the `official documentation <https://docs.balder.dev>`_ first.

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
`the contrib section of \`\`balderhub-html\`\` <https://hub.balder.dev/projects/html/en/latest/contrib/auth.html>`.

.. todo
    and [the contrib section of \`\`balderhub-http\`\`](https://hub.balder.dev/projects/http/en/latest/contrib/auth.html).

What can you do with this project?
----------------------------------

This is a BalderHub project that provides different features and scenarios for testing authentification and authorization (permissions, login, ...).


.. toctree::
    :maxdepth: 2

    installation.rst
    topic_intro.rst
    examples.rst
    scenarios.rst
    features.rst
    utilities.rst
