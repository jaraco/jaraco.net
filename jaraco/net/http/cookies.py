import http.cookiejar
import shelve


class ShelvedCookieJar(http.cookiejar.CookieJar):
    """
    Cookie jar backed by a shelf.

    Automatically persists cookies to disk.
    """

    def __init__(self, shelf: shelve.Shelf, **kwargs):
        self.shelf = shelf
        super().__init__(**kwargs)

    @property
    def _cookies(self):
        return self.shelf

    @_cookies.setter  # type: ignore
    def _cookies(self, value):
        self.shelf.clear()
        self.shelf.update(value)

    def set_cookie(self, cookie):
        with self._cookies_lock:
            # Force persistence
            d = self._cookies.setdefault(cookie.domain, {})
            d.setdefault(cookie.path, {})[cookie.name] = cookie
            self._cookies[cookie.domain] = d

    def clear(self, domain=None, path=None, name=None):
        super().clear(domain, path, name)
        if path is not None or name is not None:
            # Mark key as dirty.
            self._cookies[domain] = self._cookies[domain]
