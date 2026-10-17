import pytest

from jaraco.net.devices.base import BaseManager


def test_address_strings():
    assert BaseManager.hardware_address_to_string('\x01\xab') == '01:ab'
    assert BaseManager.ip_address_to_string('\x7f\x00\x00\x01') == '127.0.0.1'


def test_not_implemented():
    manager = BaseManager()
    with pytest.raises(NotImplementedError):
        manager.get_host_mac_addresses()
    with pytest.raises(NotImplementedError):
        manager.get_host_ip_addresses()
