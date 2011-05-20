import sys
import time
import functools

import cherrypy

def tail_f(filename):
	interval = 1.0

	with open(filename) as file:
		while True:
			where = file.tell()
			line = file.readline()
			if not line:
				time.sleep(interval)
				file.seek(where)
			else:
				yield line

def close_source():
	cherrypy.log.error("closing source")
	cherrypy.request.source.close()

cherrypy.tools.closer = cherrypy.Tool('on_end_request', close_source)

class TailedFile(object):
	"""
	A simple CherryPy controller that will tail a file and stream it to a
	browser.
	"""
	def __init__(self, filename):
		self.filename = filename

	@cherrypy.expose
	@cherrypy.tools.closer()
	def index(self):
		cherrypy.response.stream = True
		cherrypy.response.headers['content-type'] = 'text/plain'
		cherrypy.request.source = tail_f(self.filename)
		all_tails.append(cherrypy.request.source)
		return cherrypy.request.source

all_tails = []
def close_all():
	print("attempting to close all")
	for tail in all_tails:
		tail.close()

def on_signal(signal_name, handler):
	orig_handler = cherrypy.engine.signal_handler.handlers[signal_name]
	@functools.wraps(orig_handler)
	def wrapper():
		handler()
		orig_handler()
	cherrypy.engine.signal_handler.handlers[signal_name] = wrapper

if __name__ == '__main__':
	on_signal('SIGHUP', close_all)
	on_signal('SIGTERM', close_all)
	cherrypy.quickstart(TailedFile(sys.argv[1]))
