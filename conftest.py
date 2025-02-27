import functools
import importlib
import os
import platform
import socket
import sys
import time

import pytest

import jaraco.functools
from jaraco.context import ExceptionTrap

missing = ExceptionTrap(ImportError).raises


@missing
def pywin32_missing():
    importlib.import_module('win32service')


def old_ping_exception():
    """
    Ping test has different exception on older Pythons.
    """
    return sys.version_info < (3, 10)


collect_ignore = (
    [
        'jaraco/net/devices/linux.py',
        'jaraco/net/devices/win32.py',
        'jaraco/net/devices/darwin.py',
    ]
    + [
        # modules only import on Windows
        'jaraco/net/dns.py',
    ]
    * pywin32_missing()
    + [
        'jaraco/net/icmp.py',
    ]
    * old_ping_exception()
)


@pytest.fixture(autouse=True)
def retry_ntp_query(request):
    """
    ntp.query is flaky (by design), so be resilient during tests.
    """
    if not request.node.name.endswith('net.ntp.query'):
        return

    retry = jaraco.functools.retry(
        retries=4,
        trap=socket.timeout,
        cleanup=functools.partial(time.sleep, 4),
    )
    globs = request.node.dtest.globs
    globs['query'] = retry(globs['query'])
    if os.environ.get('GITHUB_ACTIONS') and platform.system != 'Linux':
        pytest.skip("Test is flaky")
