from jaraco.net.http import caching

class TestCachedResponse(object):
	def test_no_max_age(self):
		"""
		If there's no max age in the header, that should not exclude it
		from being cached.
		"""
		resp = caching.CachedResponse()
		resp.headers = {}
		assert resp.fresh()
