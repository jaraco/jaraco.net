import platform


collect_ignore = [
	'jaraco/net/dns.py',
	'jaraco/net/whois_svc.py',
] if platform.system() != 'Windows' else []
