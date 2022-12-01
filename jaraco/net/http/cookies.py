import http.cookiejar
import shelve

from . import py310compat


class FlushableShelf(shelve.DbfilenameShelf):
    """
    >>> getfixture('check_concurrent_dbm')
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
        self.filename = py310compat.fspath(filename)
        self.args = args
        self.kwargs = kwargs
        super().__init__(self.filename, *args, **kwargs)

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
        self._cookies = self.shelf = shelf

    @classmethod
    def create(cls, root, name='cookies', **kwargs):
        return cls(FlushableShelf(root / name), **kwargs)

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
