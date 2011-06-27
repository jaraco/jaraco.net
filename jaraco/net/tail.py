import sys
import time
import functools

import cherrypy.process.plugins

def tail_f(filename):
	interval = 1.0

	with open(filename) as file:
		while True:
			where = file.tell()
			line = file.readline()
			print 'read', line
			if not line:
				time.sleep(interval)
				file.seek(where)
			else:
				yield line

class TailedFile(object):
	"""
	A simple CherryPy controller that will tail a file and stream it to a
	browser.
	"""
	def __init__(self, filename):
		self.filename = filename

	@cherrypy.expose
	def index(self):
		cherrypy.response.stream = True
		cherrypy.response.headers['content-type'] = 'text/plain'
		cherrypy.request.source = tail_f(self.filename)
		cherrypy.engine.publish('register-tail')
		return cherrypy.request.source

class TailTracker(cherrypy.process.plugins.SimplePlugin, list):
	def __init__(self, bus):
		self.bus = bus
		self.bus.subscribe('register-tail', self.register)

	def register(self):
		self.append(cherrypy.request.source)

	def stop(self):
		# close all tails
		for tail in self:
			tail.close()
	stop.priority = 100

	def __hash__(self):
		return hash(id(self))

if __name__ == '__main__':
	TailTracker(cherrypy.engine).subscribe()
	cherrypy.quickstart(TailedFile(sys.argv[1]))
