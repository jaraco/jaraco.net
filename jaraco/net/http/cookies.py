import pathlib
import collections
import http.cookiejar
import contextlib

import jsonpickle


class Shelf(collections.abc.MutableMapping):
    """
    Similar to Python's shelve.Shelf, implements a persistent
    dictionary using jsonpickle.

    >>> fn = getfixture('tmp_path') / 'shelf.json'
    >>> shelf = Shelf(fn)
    >>> shelf['foo'] = 'bar'
    >>> copy = Shelf(fn)
    >>> copy['foo']
    'bar'
    >>> shelf['bar'] = 'baz'
    >>> Shelf(fn)['bar']
    'baz'
    """

    def __init__(self, filename):
        self.filename = pathlib.Path(filename)
        self.store = dict()
        with contextlib.suppress(Exception):
            self._load()

    def _load(self):
        self.store = jsonpickle.decode(self.filename.read_text())

    def _save(self):
        self.filename.write_text(jsonpickle.encode(self.store))

    def __getitem__(self, *args, **kwargs):
        return self.store.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        self.store.__setitem__(*args, **kwargs)
        self._save()

    def __delitem__(self, *args, **kwargs):
        self.store.__delitem__(*args, **kwargs)
        self._save()

    def __iter__(self):
        return self.store.__iter__()

    def __len__(self):
        return self.store.__len__()


class ShelvedCookieJar(http.cookiejar.CookieJar):
    """
    Cookie jar backed by a shelf.

    Automatically persists cookies to disk.
    """

    def __init__(self, shelf: Shelf, **kwargs):
        super().__init__(**kwargs)
        self._cookies = shelf

    @classmethod
    def create(cls, root, name='cookies.json', **kwargs):
        return cls(Shelf(root / name), **kwargs)

    def set_cookie(self, cookie):
        with self._cookies_lock:
            self._cookies.setdefault(cookie.domain, {}).setdefault(cookie.path, {})[
                cookie.name
            ] = cookie
            self._cookies._save()

    def clear(self, domain=None, path=None, name=None):
        super().clear(domain, path, name)
        if path is not None or name is not None:
            self._cookies._save()

    def get(self, name, default=None):
        matches = (
            cookie
            for domain in self._cookies
            for cookie in self._cookies[domain]
            if cookie.name == name
        )
        return next(matches, default)
