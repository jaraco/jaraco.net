#!python

# $Id$

"""
  scanner.py

TCP port scanning utility
"""

import os, operator, sys
import re, struct, socket, itertools
from optparse import OptionParser

import inet
from jaraco.util import TimestampFileHandler

import logging
log = logging.getLogger('port scanner')

def GetParser():
	usage = 'usage: %prog [options]'
	parser = OptionParser(usage)
	parser.add_option('-l', '--logging-level',
					   help="Set the logging level (DEBUG, INFO, WARNING, ERROR)",
					   default = 'INFO')
	parser.add_option('-o', '--host-spec',
					   help="The host range or host range to scan",
					   default = r'localhost')
	parser.add_option('-p', '--port-range',
					   help="Port range to scan",
					   default = '[25,80]')
	parser.add_option('-f', '--frequency', default = 20, type="int",
					   help="Frequency (Hz) of connection attempt")
	description=  """No Description"""
	return parser
	
def setupLogger(output_level):
	outputHandler = logging.StreamHandler(sys.stdout)
	outputHandler.level = getattr(logging, output_level.upper())
	logging.root.handlers.append(outputHandler)
	logbase = os.path.join(os.environ['SystemRoot'], 'system32', 'logfiles', 'portscan', 'scan.log')
	logfilehandler = TimestampFileHandler(logbase)
	logfilehandler.level = logging.INFO
	handlerFormat = '[%(asctime)s] - %(levelname)s - [%(name)s] %(message)s'
	formatter = logging.Formatter(handlerFormat)
	logfilehandler.setFormatter(formatter)
	logging.root.handlers.append(logfilehandler )
	logging.root.level = 0

def _get_mask_host(host_spec, matcher):
	addr = struct.unpack('!L', socket.inet_aton(matcher.group(1)))[0]
	bits = 32 - int(matcher.group(2))
	mask = ((1 << 32) - 1) ^ ((1 << bits) - 1)
	if (0xFFFFFFFF ^ mask) & addr:
		log.warning('Bits lost in mask')
	base = addr & mask
	addrs = xrange(1 << bits)
	result = itertools.imap(operator.or_, addrs, itertools.repeat(base))
	result = itertools.imap(lambda a: struct.pack('!L', a), result)
	return itertools.imap(socket.inet_ntoa, result)

def _get_range_host(host_spec, matcher):
	#matcher = matcher.next()
	rng = map(int, matcher.groups())
	rng[1] += 1
	rng = range(*rng)
	beg = host_spec[:matcher.start()]
	end = host_spec[matcher.end():]
	addrs = itertools.chain(*itertools.imap(lambda n: get_hosts(beg + str(n) + end), rng))
	return addrs

def get_hosts(host_spec):
	_map = {'([\d\.]+)/(\d+)': ('match', _get_mask_host),
			'(\d+)-(\d+)': ('search', _get_range_host)}
	for pattern in _map:
		test, func = _map[pattern]
		matcher = getattr(re, test)(pattern, host_spec)
		if matcher:
			return func(host_spec, matcher)
	return (host_spec,)

def scan():
	parser = GetParser()
	options, args = parser.parse_args()
	if not len(args) == 0:
		parser.error('Incorrect number of arguments supplied')
		sys.exit(1)
	setupLogger(options.logging_level)
	try:
		ports = eval(options.port_range)
		hosts = get_hosts(options.host_spec)
		inet.portscan_hosts(hosts, ports, options.frequency)
		inet.ScanThread.waitForTestersToFinish()
	except KeyboardInterrupt:
		log.info('Terminated by user')
	except:
		log.exception('Fatal error occured.  Terminating.')

if __name__ == '__main__':
	scan()