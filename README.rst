.. image:: https://img.shields.io/pypi/v/jaraco.net.svg
   :target: https://pypi.org/project/jaraco.net

.. image:: https://img.shields.io/pypi/pyversions/jaraco.net.svg

.. image:: https://github.com/jaraco/jaraco.net/workflows/tests/badge.svg
   :target: https://github.com/jaraco/jaraco.net/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. image:: https://readthedocs.org/projects/jaraconet/badge/?version=latest
   :target: https://jaraconet.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2023-informational
   :target: https://blog.jaraco.com/skeleton

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
