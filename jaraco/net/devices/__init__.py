"""
>>> mgr = Manager()
>>> all(map(len, mgr.get_host_ip_addresses()))
True
>>> all(map(len, mgr.get_host_mac_addresses()))
True
"""

import sys

try:
    __mod = __import__(__name__ + '.' + sys.platform, fromlist=['Manager'])
    Manager = __mod.Manager
except ImportError:
    from .base import BaseManager as Manager  # noqa
