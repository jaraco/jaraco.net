import cherrypy
import sys
import time

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
	print("closing source")
	cherrypy.error("closing source")
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
		return cherrypy.request.source

if __name__ == '__main__':
	cherrypy.quickstart(TailedFile(sys.argv[1]))
