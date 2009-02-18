#!python

# $Id$

import sys
import socket

def lookup_host(host):
	ip = socket.gethostbyname(host)

	reversed_ip = '.'.join(reversed(ip.split('.')))

	for bl in ('zen.spamhaus.org', 'ips.backscatterer.org', 'bl.spamcop.net', 'list.dsbl.org'):
		lookup = '.'.join((reversed_ip, bl))
		try:
			res = socket.gethostbyname(lookup)
			print host, 'listed with', bl, 'as', res
		except socket.gaierror:
			pass

def handle_cmdline():
	lookup_host(sys.argv[1])

if __name__ == '__main__':
	handle_cmdline()