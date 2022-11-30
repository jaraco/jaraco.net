import sys
import platform


collect_ignore = (
    [
        'jaraco/net/devices/linux2.py',
        'jaraco/net/devices/win32.py',
    ]
    + [
        # modules only import on Windows
        'jaraco/net/dns.py',
        'jaraco/net/whois_svc.py',
    ]
    * (platform.system() != 'Windows')
    + [
        # fabric fails on Python 3.11
        'fabfile.py',
    ]
    * (sys.version_info > (3, 11))
)
