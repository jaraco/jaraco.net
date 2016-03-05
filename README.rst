.. -*- restructuredtext -*-

jaraco.net
==========

.. contents::

Status and License
------------------

``jaraco.net`` provides miscellaneous utility functions used across
projects developed by the author.

``jaraco.net`` is written by Jason R. Coombs.  It is licensed under an
`MIT-style permissive license
<http://www.opensource.org/licenses/mit-license.php>`_.

You can install it with ``easy_install jaraco.net`` or check out the source
from
`the mercurial repository <https://bitbucket.org/jaraco/jaraco.net>`_.

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
