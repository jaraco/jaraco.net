# -*- coding: UTF-8 -*-

""" Setup script for building jaraco.net

Copyright © 2009 Jason R. Coombs
"""

__author__ = 'Jason R. Coombs <jaraco@jaraco.com>'
__version__ = '$Rev$'[6:-2]
__svnauthor__ = '$Author$'[9:-2]
__date__ = '$Date$'[7:-2]

try:
	from distutils.command.build_py import build_py_2to3 as build_py
	# exclude some fixers that break already compatible code
	from lib2to3.refactor import get_fixers_from_package
	fixers = get_fixers_from_package('lib2to3.fixes')
	for skip_fixer in ['import']:
		fixers.remove('lib2to3.fixes.fix_' + skip_fixer)
	build_py.fixer_names = fixers
except ImportError:
	from distutils.command.build_py import build_py

from setuptools import setup, find_packages

try:
	from jaraco.util.package import read_long_description
	long_description = read_long_description()
except:
	long_description = None

setup(
	name = 'jaraco.net',
	version = '1.1',
	description = 'Networking tools by jaraco',
	long_description = long_description,
	author = 'Jason R. Coombs',
	author_email = 'jaraco@jaraco.com',
	url = 'http://www.jaraco.com/',
	packages = find_packages(exclude=['ez_setup', 'tests', 'examples']),
	namespace_packages = ['jaraco',],
	license = 'MIT',
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"Programming Language :: Python",
	],
	entry_points = {
		'console_scripts': [
			'whois-bridge = jaraco.net.whois:main',
			'scanner = jaraco.net.scanner:scan',
			'fake-http = jaraco.net.http:start_simple_server',
			'fake-http-auth = jaraco.net.http:auth_request_server',
			'wget = jaraco.net.http:wget',
			'fake-smtp = jaraco.net.smtp:start_simple_server',
			'udp-send = jaraco.net.udp:Sender',
			'udp-echo = jaraco.net.udp:EchoServer',
			'dns-forward-service = jaraco.net.dns:start_service',
			'dnsbl-check = jaraco.net.dnsbl:handle_cmdline',
			'ntp = jaraco.net.ntp:handle_command_line',
			'remove-known-spammers = jaraco.net.email:remove_known_spammers',
			'tcp-test-connect = jaraco.net.tcp:test_connect',
			],
	},
	install_requires=[
		'jaraco.util',
		'clientform>=0.2.7',
		'BeautifulSoup',
	],
	extras_require = {
	},
	dependency_links = [
	],
	tests_require=[
		'nose>=0.10',
	],
	test_suite = "nose.collector",
	cmdclass=dict(build_py=build_py),
)
