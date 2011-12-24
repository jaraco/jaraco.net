"""
dnsbl: DNS blocklist support
"""

from __future__ import print_function

import sys
import socket
import argparse

class BlocklistHit(object):
	def __init__(self, host, blocklist, result):
		self.host = host
		self.blocklist = blocklist
		self.result = result

	def __str__(self):
		return "{host} listed with {blocklist} as {result}".format(**vars(self))

class Server(unicode):
	@staticmethod
	def reverse_ip(ip):
		return '.'.join(reversed(ip.split('.')))

	def lookup(self, host):
		ip = socket.gethostbyname(host)
		rev_ip = self.reverse_ip(ip)
		key = '.'.join((rev_ip, self))
		try:
			res = socket.gethostbyname(key)
			print(host, 'listed with', self, 'as', res)
		except socket.gaierror:
			return
		return BlocklistHit(host, self, res)

	@classmethod
	def handle_command_line(cls):
		parser = argparse.ArgumentParser()
		parser.add_argument('host')
		args = parser.parse_args()
		cls.lookup_all(args.host)

	@staticmethod
	def lookup_all(host):
		for server in blocklist_servers:
			res = server.lookup(host)
			if res: print(res)

blocklist_servers = map(Server, [
	'dnsbl.jaraco.com',
	'zen.spamhaus.org',
	'ips.backscatterer.org',
	'bl.spamcop.net',
	'list.dsbl.org',
])

if __name__ == '__main__':
	Server.handle_command_line()
