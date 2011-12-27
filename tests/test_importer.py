import contextlib
import logging
import sys

from jaraco.net import importer

@contextlib.contextmanager
def logging_context(**kwargs):
	"""
	Creating a logging context using logging.basicConfig.
	"""
	orig_handlers = logging.root.handlers
	logging.root.handlers[:] = []
	try:
		logging.basicConfig(**kwargs)
		yield
	finally:
		logging.root.handlers[:] = orig_handlers

def test_importer():
	with logging_context(level=logging.DEBUG):
		importer.URLImporter.install()
		sys.path.append('http://python-distribute.org/')
		try:
			import distribute_setup
		finally:
			importer.URLImporter.remove()
