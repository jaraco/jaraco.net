#!python

import os

import pytest

test_dir = os.path.dirname(__file__)


@pytest.mark.skipif(True, reason="Test can't run on Python 3")
def test_bolivia_handler():
    from jaraco.net.whois import BoliviaWhoisHandler

    handler = BoliviaWhoisHandler('microsoft.com.bo')
    handler.client_address = '127.0.0.1'
    test_result = os.path.join(test_dir, 'nic.bo.html')
    handler._response = open(test_result).read()
    result = handler.ParseResponse()
    assert 'Microsoft Corporation' in result
