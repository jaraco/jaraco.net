.. image:: https://img.shields.io/pypi/v/skeleton.svg
   :target: https://pypi.org/project/skeleton

.. image:: https://img.shields.io/pypi/pyversions/skeleton.svg

.. image:: https://img.shields.io/travis/jaraco/skeleton/master.svg
   :target: https://travis-ci.org/jaraco/skeleton

.. .. image:: https://img.shields.io/appveyor/ci/jaraco/skeleton/master.svg
..    :target: https://ci.appveyor.com/project/jaraco/skeleton/branch/master

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

``jaraco.net`` provides miscellaneous utility functions used across
projects developed by the author.

DNS Forwarding Service
----------------------

``jaraco.net`` includes a DNS forwarding service for Windows. This is
because Microsoft appears to be unable to bind to 6 to 4 and Teredo
addresses with their production DNS Server. After installing
``jaraco.net``, the service executable is available as
`%PYTHON%\Scripts\dns-forward-service.exe`. In addition to the
documented install/uninstall/start/stop commands, it's also possible
to configure a bind address with the -b option. For example::

    dns-forward-service -b 2002:41de:a625::41de:a625 install

The service will be installed and the bind address will be stored in
`HKLM\Software\jaraco.net\DNS Forwarding Service\Listen Address`. Note
that the service must be restarted to recognize an updated bind address.
