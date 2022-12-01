import jaraco.context

import http.cookiejar
import shelve


class FlushableShelf(shelve.DbfilenameShelf):
    """
    >>> fn = getfixture('tmp_path') / 'shelf'
    >>> shelf = FlushableShelf(fn)
    >>> shelf['foo'] = 'bar'
    >>> shelf.flush()
    >>> copy = FlushableShelf(fn)
    >>> copy['foo']
    'bar'
    >>> shelf['bar'] = 'baz'
    >>> shelf.flush()
    >>> FlushableShelf(fn)['bar']
    'baz'
    """

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        self.args = args
        self.kwargs = kwargs
        super().__init__(filename, *args, **kwargs)

    def flush(self):
        self.close()
        super().__init__(self.filename, *self.args, **self.kwargs)


class ShelvedCookieJar(http.cookiejar.CookieJar):
    """
    Cookie jar backed by a shelf.

    Automatically persists cookies to disk.
    """

    def __init__(self, shelf: FlushableShelf, **kwargs):
        super().__init__(**kwargs)
        self.shelf = shelf

    @property
    def _cookies(self):
        return self.shelf

    @_cookies.setter  # type: ignore
    # bypass during initialization
    @jaraco.context.suppress(AttributeError)
    def _cookies(self, value):
        self.shelf.clear()
        self.shelf.update(value)
        self.shelf.flush()

    def set_cookie(self, cookie):
        with self._cookies_lock:
            # Force persistence
            d = self._cookies.setdefault(cookie.domain, {})
            d.setdefault(cookie.path, {})[cookie.name] = cookie
            self._cookies[cookie.domain] = d
            self.shelf.flush()

    def clear(self, domain=None, path=None, name=None):
        super().clear(domain, path, name)
        if path is not None or name is not None:
            # Mark key as dirty.
            self._cookies[domain] = self._cookies[domain]
        self.shelf.flush()

    def get(self, name, default=None):
        matches = (
            cookie
            for domain in self._cookies
            for cookie in self._cookies[domain]
            if cookie.name == name
        )
        return next(matches, default)
