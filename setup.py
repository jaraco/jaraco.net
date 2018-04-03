#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io
import sys

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

name = 'jaraco.net'
description = 'Networking tools by jaraco'
nspkg_technique = 'managed'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

windows_scripts = [
	'whois-bridge-service = jaraco.net.whois:Service.handle_command_line',
	'wget = jaraco.net.http:wget',
] if sys.platform == 'win32' else []

params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/jaraco/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=(
		name.split('.')[:-1] if nspkg_technique == 'managed'
		else []
	),
	python_requires='>=2.7',
	install_requires=[
		'more_itertools',
		'BeautifulSoup4',
		'keyring>=0.6',
		'lxml',
		'requests',
		'feedparser',
		'six>=1.4',
		'backports.method_request',
		'jaraco.text',
		'jaraco.logging',
		'jaraco.email',
		'jaraco.path',
		'path.py',
	],
	extras_require={
		'testing': [
			# upstream
			'pytest>=3.5',
			'pytest-sugar>=0.9.1',
			'collective.checkdocs',
			'pytest-flake8',

			# local
			'cherrypy',
			'svg.charts',
		],
		'docs': [
			# upstream
			'sphinx',
			'jaraco.packaging>=3.2',
			'rst.linker>=1.9',

			# local
		],
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
	],
	entry_points={
		'console_scripts': [
			'whois-bridge = jaraco.net.whois:serve',
			'scanner = jaraco.net.scanner:scan',
			'fake-http = jaraco.net.http.servers:Simple.start',
			'fake-http-auth = jaraco.net.http.servers:AuthRequest.start',
			'serve-local = jaraco.net.http.static:serve_local',
			'fake-smtp = jaraco.net.smtp:start_simple_server',
			'udp-send = jaraco.net.udp:Sender',
			'udp-echo = jaraco.net.udp:EchoServer',
			(
				'dns-forward-service = '
				'jaraco.net.dns:ForwardingService.handle_command_line'
			),
			'dnsbl-check = jaraco.net.dnsbl:Service.handle_command_line',
			'ntp = jaraco.net.ntp:handle_command_line',
			'remove-known-spammers = jaraco.net.email:remove_known_spammers',
			'tcp-test-connect = jaraco.net.tcp:test_connect',
			'tcp-echo-server = jaraco.net.tcp:start_echo_server',
			'http-headers = jaraco.net.http:headers',
			'build-dir-index = jaraco.net.site:make_index_cmd',
			'content-type-reporter = jaraco.net.http.content:ContentTypeReporter.run',
			'web-tail = jaraco.net.tail:handle_command_line',
			'rss-launch = jaraco.net.rss:launch_feed_enclosure',
			'rss-download = jaraco.net.rss:download_enclosures',
		] + windows_scripts,
	},
)
if __name__ == '__main__':
	setuptools.setup(**params)
