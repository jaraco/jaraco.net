import socket
from optparse import OptionParser

def get_connect_options():
	parser = OptionParser(conflict_handler="resolve")
	parser.add_option('-h', '--host', default='localhost')
	parser.add_option('-p', '--port', default=80, type='int')
	options, args = parser.parse_args()
	if not len(args) == 0:
		parser.error("Unexpected positional argument")
	return options

def test_connect():
	options = get_connect_options()
	addr = options.host, options.port
	family, socktype, proto, canonname, sockaddr = socket.getaddrinfo(*addr)[0]
	sock = socket.socket(family, socktype, proto)
	try:
		conn = sock.connect(sockaddr)
	except socket.error as e:
		print e
		raise SystemExit(1)
	args = vars(options)
	print "Successfully connected to {host} on port {port}".format(**args)
	