import sys
import importlib
import os
import dbm

import pytest
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


@pytest.fixture(scope='session')
def check_concurrent_dbm(tmp_path_factory):
    """
    Some environments dissallow concurrent access on DBM files.

    Detect such environments and skip those tests.
    """
    name = tmp_path_factory.mktemp("dbm check") / 'data'
    orig = dbm.open(os.fspath(name), flag='c')  # noqa: F841
    try:
        dbm.open(os.fspath(name))
    except Exception:
        pytest.skip("Unable to open dbm concurrently")
