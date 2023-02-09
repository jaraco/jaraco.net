v9.3.1
======

Fix ``EncodingWarnings``.

v9.3.0
======

Prefer ``email`` to deprecated ``cgi`` module.

v9.2.0
======

#4: Added support for macOS to ``jaraco.net.devices``.

v9.1.0
======

Allow a ``ShelvedCookieJar`` to be created in the current directory
by default.

v9.0.1
======

Fixed ``AttributeError`` in ``ShelvedCookieJar.get``.

v9.0.0
======

#2: ``http.cookies`` no longer relies on ``shelve.Shelf``, but instead
provides its own ``Shelf`` implementation that automatically persists
any cookies.

v8.0.0
======

#1: Added ``http.cookies`` module with a persistent ``ShelvedCookieJar``.

Substantial cleanup with some functionality removed. Removed dependencies
on expensive packages (``pyobjc``, ``pywin32``).

v7.1.0
======

Require Python 3.6 or later.

v7.0.0
======

Drop support for Python 3.5 and earlire.

6.0
===

Removed deprecated modules:

 - ``jaraco.net.email``
 - ``jaraco.net.smtp``
 - ``jaraco.net.notification``

Switch to `pkgutil namespace technique
<https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages>`_
for the ``jaraco`` namespace.

5.3
===

Refresh package metadata.

5.2
===

Remove dependency on jaraco.util.

5.1
===

Deprecated email modules and moved them to jaraco.email.

5.0
===

Drop support for Python 2.6

4.0.1
=====

* Fixed encoding issue in SMTPNotifier.

4.0
===

* Removed ``http.MethodRequest``. Use `backports.method_request
  <https://pypi.python.org/pypi/backports.method_request/>`_ instead.

3.0
===

* Removed ``wget`` command except on Windows.

2.1
===

* Added '--outfile' parameter to fake-http.
* Fixed bug in http caching support when max-age is not specified.

2.0
===

* Added `jaraco.net.http.MethodRequest`, a urllib2.Request subclass which takes
  a 'method' parameter.
* Consolidated many functions from jaraco.net.http to classes in
  `jaraco.net.http.servers`.
* `whois-bridge` now runs the daemon. A new script `whois-bridge-service` is
  installed on Windows only and specifically invokes the service.
* Removed `cookies` module.
* Refactored `dnsbl` module. Replaced `lookup_host` with `Service.lookup_all`.
  See the module for other interface changes.
* Removed `headers` module (was experimental, now abandoned).
* Removed `html` module (it depends on htmllib, which was deprecated).

1.7
===

* Added web-tail command, which "tails" a file, serving the content over
  http to multiple clients (requires CherryPy).

1.6
===

* Added jaraco.net.importer, featuring URLImporter.
* Added jaraco.net.http.content.ContentTypeReporter, a cherrypy app to
  report the content type of uploaded content.

1.5.1
=====

* Added directory listing support to serve-local.

1.5
===

* Added simple script for creating a directory index (used for legacy
  support).
* Added command script "serve-local" which uses cherrypy to serve the
  current directory on port 8080.

1.4
===

* Fixed issue where passing a numeric host to scanner would be detected
  as a named host.
* Fixed HTTP server to work with multipart requests.
* Pickling in http.cache.CachedResponse is now less depedent on the actual
  implementation.
* Added tail module that utilizes CherryPy to serve the tail of a file.
* Fixed issue in setup script with deprecated hgtools usage.
* Using argparse and enabling logging config in ntp module.

1.3
===

* Added jaraco.net.devices package. Includes a Manager class for
  retrieving MAC addresses and IP addresses on the host.
* Created jaraco.net.http package (from module of the same name)
* Added jaraco.net.http.caching, an early attempt at providing a
  CachingHandler for urllib2 with HTTP protocol support.
* Added a simple echo server.
* Added http-headers command.

1.2
===

* Added function wait_for_host to icmp lib
* Added support for a custom bind address to the DNS Forwarding Service

1.1
===

* Added rss module (migrated from jaraco.util)

1.0
===

* Initial release.
