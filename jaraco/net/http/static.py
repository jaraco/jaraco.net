import cherrypy
import os

def serve_local():
	"""
	Serve the current directory as static files.
	"""
	config = {
		'global': {
			'server.socket_host': '::0',
		},
		'/': {
			'tools.staticdir.root': os.getcwd(),
			'tools.staticdir.on': 'true',
			'tools.staticdir.dir': '.',
		},
	}
	cherrypy.quickstart(None, config=config)
