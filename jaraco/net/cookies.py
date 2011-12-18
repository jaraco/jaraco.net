# -*- coding: UTF-8 -*-

"""cookies.py
Implements cookie support.
This works better than the library supplied in Python.

Copyright © 2004, 2011 Jason R. Coombs
"""


import os
import copy
import urllib
import httplib
import itertools
import string
import re

# import case-insensitive string & dictionary
from jaraco.util.string import FoldedCase
from jaraco.util.dictlib import FoldedCaseKeyedDict

class CookieMonster(object):
	"Read cookies out of a user's IE cookies file"

	@property
	def cookie_dir(self):
		import _winreg as winreg
		key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, 'Software'
			'\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
		cookie_dir, type = winreg.QueryValueEx(key, 'Cookies')
		return cookie_dir

	def entries(self, filename):
		with open(os.path.join(self.cookie_dir, filename)) as cookie_file:
			while True:
				entry = itertools.takewhile(self.is_not_cookie_delimiter,
					cookie_file)
				entry = map(string.rstrip, entry)
				if not entry: break
				cookie = self.make_cookie(*entry)
				yield cookie

	@staticmethod
	def is_not_cookie_delimiter(s):
		return s != '*\n'

	@staticmethod
	def make_cookie(key, value, domain, flags, ExpireLow, ExpireHigh,
		CreateLow, CreateHigh):
		expires = (int(ExpireHigh) << 32) | int(ExpireLow)
		created = (int(CreateHigh) << 32) | int(CreateLow)
		del ExpireHigh, ExpireLow, CreateHigh, CreateLow
		flags = int(flags)
		domain, path = string.split(domain, '/', 1)
		path = '/' + path
		cookie = vars()
		return cookie

def getCookies(source, path=None):
	"""
	Takes a Set-Cookie header (possibly with multiple cookies) or multiple
	Set-Cookie headers, and returns a list of cookies in those headers.
	`source` may be an httplib.HTTPResponse or httplib.HTTPMessage or a list
	of Set-Cookie headers or a Set-Cookie header.

	>>> getCookies('A=B, C=D')
	[<cookie A=B, C=D>]

	>>> getCookies(['A=B', 'C=D'])
	[<cookie A=B>, <cookie C=D>]
	"""
	result = []
	if isinstance(source, httplib.HTTPResponse):
		source = source.msg
	if isinstance(source, httplib.HTTPMessage):
		source = source.getheaders('Set-Cookie')
	if isinstance(source, (list, tuple)):
		map(result.extend, map(getCookies, source, (path,)*len(source)))
	elif isinstance(source, str):
		c = cookie(source)
		path and c.setPathIfEmpty(path)
		result.append(c)
	return result

class cookie(object):
	"""
	cookie class parses cookie information from HTTP Responses and outputs
	for HTTP Requests
	"""
	parameterNames = tuple(map(FoldedCase, ('expires', 'path', 'domain', 'secure')))
	def __init__(self, source = None):
		if isinstance(source, basestring):
			self.readFromSetHeader(source)
		if isinstance(source, self.__class__):
			self.__dict__ = source.__dict__.copy()

	def readFromSetHeader(self, header):
		'Read a cookie from a header as received in an HTTP Response'
		if hasattr(self, '__name'):
			raise RuntimeError, 'Cookies may not be re-used.'
		fields = re.split(';\s*', header)
		splitEquals = lambda x: x.split('=', 1)
		fieldPairs = map(splitEquals, fields)
		self.__parameters = FoldedCaseKeyedDict(fieldPairs)
		self.__findName()

	def __findName(self):
		"Find the name of the cookie, which should be the only pair that's not a parameter"
		isNotParameter = lambda k: k not in self.parameterNames
		names = filter(isNotParameter, self.__parameters)
		if not len(names) == 1:
			raise ValueError, "Found more than one name/value pair where name isn't a cookie parameter %s" % names
		name = names[0]
		self.__name = name
		self.__value = self.__parameters[name]
		del self.__parameters[name]

	def getRequestHeader(self):
		"returns the cookie as can be used in an HTTP Request"
		return '='.join((self.__name, self.__value))

	def isSecure(self):
		return eval(string.capwords(self.__parameters.get('secure', 'False')))

	def __eq__(self, other):
		"Instances of the same path and name will overwrite each other."
		samepath = self.getPath() == other.getPath()
		return self.__name == other.__name and samepath

	def getPath(self):
		return self.__parameters.get('path', '')

	def getParameters(self):
		return self.__parameters

	def get(self, *args):
		return self.__parameters.get(*args)

	def setPathIfEmpty(self, path):
		if not self.getPath():
			self.__parameters['path'] = path

	def __str__(self):
		return 'Cookie: ' + self.__parameterString()

	def __repr__(self):
		return '<%s %s>' % (self.__class__.__name__, self.__parameterString())

	def __parameterString(self):
		return '; '.join(map('='.join, [(self.__name, self.__value)] + self.__parameters.items()))

class Container(set):
	"""
	An object for storing cookies as a web browser would.

	>>> cn = Container()
	>>> c1 = cookie('bar=baz; expires=2011-12-17T21:09:00; path=/foo')
	>>> c2 = cookie('bar=biz; expires=2011-12-17T21:10:00')
	>>> cn.add(c1)
	>>> cn.add(c2)
	>>> cn.add(c1)
	>>> len(cn)
	2
	>>> cn.get_request_header()
	u'bar=baz; bar=biz'
	"""

	def get_request_header(self, test = lambda x: True):
		"return the cookies for which test(cookie) == True"
		delimiter = '; '
		matched_cookies = filter(test, self)
		# Sort the cookies such that cookies with a path of /bar appear before
		#  cookies with a path of /.
		matched_cookies.sort(key = lambda cookie: cookie.getPath(),
			reverse=True)
		strings = [cookie.getRequestHeader() for cookie in matched_cookies]
		return delimiter.join(strings)

	def add(self, cookie):
		"""
		Add cookie or cookies to this container.
		"""
		if isinstance(cookie, (tuple, list)):
			map(self.add, cookie)
			return
		super(Container, self).add(cookie)
