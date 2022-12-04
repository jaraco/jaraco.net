import sys
import importlib

from jaraco.context import ExceptionTrap


missing = ExceptionTrap(ImportError).raises


@missing
def pywin32_missing():
    importlib.import_module('win32service')


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
    * pywin32_missing()
    + [
        # fabric fails on Python 3.11
        'fabfile.py',
    ]
    * (sys.version_info > (3, 11))
)
