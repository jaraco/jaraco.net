import platform


windows_ignore = (
    ['jaraco/net/dns.py', 'jaraco/net/whois_svc.py']
    if platform.system() != 'Windows'
    else []
)


collect_ignore = [
    'jaraco/net/devices/linux2.py',
    'jaraco/net/devices/win32.py',
] + windows_ignore
