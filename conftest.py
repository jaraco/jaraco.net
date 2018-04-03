import platform


collect_ignore = [
	'jaraco/net/dns.py',
] if platform.system() != 'Windows' else []
