import email
import types

from jaraco.net.http import caching


class TestCachedResponse:
    def test_no_max_age(self):
        """
        If there's no max age in the header, that should not exclude it
        from being cached.
        """
        resp = caching.CachedResponse()
        resp.headers = {}
        assert resp.fresh()

    def test_max_age_zero_in_response(self):
        """
        If max-age is zero, it should never be fresh.
        """
        resp = caching.CachedResponse()
        resp.headers = {'date': email.utils.formatdate(), 'cache-control': 'max-age=0'}
        assert not resp.fresh()

    def test_max_age_zero_in_request(self):
        """
        If max-age is zero, it should never be fresh.
        """
        resp = caching.CachedResponse()
        resp.headers = {'date': email.utils.formatdate()}
        assert resp.fresh()
        req_headers = {'cache-control': 'max-age=0'}

        assert not resp.fresh_for(req_headers)


def test_should_cache():
    def response(**headers):
        return types.SimpleNamespace(headers=headers)

    handler = caching.CacheHandler(store=None)
    assert handler.should_cache(response())
    assert not handler.should_cache(response(range='bytes=0-1'))
    assert not handler.should_cache(response(vary='accept'))


def test_defrag_uri():
    assert (
        caching.CacheHandler._defrag_uri('http://host/path#frag') == 'http://host/path'
    )
