import cherrypy
import sys
import time

def tail_f(file):
	interval = 1.0

	while True:
		where = file.tell()
		line = file.readline()
		if not line:
			time.sleep(interval)
			file.seek(where)
		else:
			yield line


class TailedFile(object):
	def __init__(self, filename):
		self.filename = filename

	@cherrypy.expose
	def index(self):
		cherrypy.response.stream = True
		cherrypy.response.headers['content-type'] = 'text/plain'
		return tail_f(open(self.filename))

if __name__ == '__main__':
	cherrypy.quickstart(TailedFile(sys.argv[1]))
