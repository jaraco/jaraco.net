#!/usr/bin/env python

# $Id$

from socket import *
import struct
import sys
import time
import logging
from jaraco.util import trim

log = logging.getLogger(__name__)

TIME1970 = 2208988800L		# Thanks to F.Lundh

def query(server, force_ipv6=False):
	timeout = 3
	ntpport = 123

	args = [server, ntpport]
	if force_ipv6:
		args.append(AF_INET6)
	
	infos = getaddrinfo(*args)

	log.debug(infos)
	family, socktype, proto, canonname, sockaddr = infos[0]
	socktype = SOCK_DGRAM

	log.info('Requesting time from %(sockaddr)s' % vars())
	client = socket(family=family, type=socktype, proto=proto)
	client.settimeout(timeout)
	
	data = '\x1b' + 47 * '\0'
	client.sendto(data, sockaddr)
	data, address = client.recvfrom(1024)
	if data:
		log.info('Response received from: %s', address)
		t = struct.unpack('!12I', data)[10]
		t -= TIME1970
		log.info('\tTime=%s', time.ctime(t))

def handle_command_line():
	"""
	%prog [options] ntp-server
	
	Query the NTP server for the current time.
	"""
	logging.basicConfig(level=logging.INFO, format="%(message)s")
	from optparse import OptionParser
	parser = OptionParser(usage=trim(handle_command_line.__doc__))
	parser.add_option('-6', '--ipv6', help="Force IPv6", action="store_true", default=False)
	options, args = parser.parse_args()
	server = args.pop()
	if args: parser.error('Too many arguments supplied')
	query(server, options.ipv6)

if __name__ == '__main__': handle_command_line()