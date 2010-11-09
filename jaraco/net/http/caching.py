"""
urllib2 HTTP caching support
inspired by http://code.activestate.com/recipes/491261/
"""

import pickle
import urllib2
from StringIO import StringIO

class CacheHandler(urllib2.BaseHandler):
	"""
	Stores responses in a httplib2-style cache object.
	"""
	def __init__(self, store):
		"construct a handler from a store"
		self.store = store

	def default_open(self, request):
		"""
		Open the url specified in the request. If it's an HTTP GET, and
		the result is a valid cached value, return the cached version.
		"""
		url = request.get_full_url()
		if request.get_method() in ('PUT',):
			# invalate this item if cached
			self.store.delete(url)
		if request.get_method() is not 'GET':
			# defer to other handlers
			return None
		
		return CachedResponse.load(self.store.get(url))

	def http_response(self, request, response):
		"""
		Gets a HTTP response. If it was a normal response (200 level) to
		a GET request, store it in the cache.
		"""
		is_get = request.get_method() == 'GET'
		if not (
			request.get_method() == "GET"
			and 200 <= response.code < 300
		): return response

		if self.should_cache(response):
			response = CachedResponse(response)
			self.store.set(request.get_full_url(), response.save())
		return response

	def should_cache(self, response):
		# todo: respect the headers
		return not getattr(response, 'cached', False)

class CachedResponse(StringIO):
	"""
	A response object compatible with urllib2.response objects but for
	cached responses.
	"""
	cached = True
	def __init__(self, response):
		#super(CachedResponse, self).__init__(response.read())
		StringIO.__init__(self, response.read())
		self.seek(0)
		self.headers = response.info()
		self.url = response.url
		self.code = response.code
		self.msg = response.msg

	def save(self):
		self.headers['x-urllib2-cache'] = 'Stored'
		return pickle.dumps(self)

	@classmethod
	def load(cls, payload):
		if payload is None:
			return None
		result = pickle.loads(payload)
		result.headers['x-urllib2-cache'] = 'Cached'
		return result

	def info(self):
		return self.headers

	def geturl(self):
		return self.url

	def reload(self, store):
		opener = urllib2.build_opener()
		self.__init__(opener.open(self.url))
		store.set(self.url, self.save())

def quick_test():
	"""Quick test/example of CacheHandler"""
	from httplib2 import FileCache
	store = FileCache(".cache")
	opener = urllib2.build_opener(CacheHandler(store))
	urllib2.install_opener(opener)
	response = opener.open("http://google.com")
	print response.headers
	print "Response:", response.read()[:100]

	response.reload(store)
	print response.headers
	print "After reload:", response.read()[:100]

if __name__ == "__main__":
	quick_test()
