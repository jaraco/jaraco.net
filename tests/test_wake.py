import socket

from jaraco.net import wake


def test_wake_on_lan(monkeypatch):
    sent = []

    class FakeSocket:
        def __init__(self, *args):
            pass

        def setsockopt(self, *args):
            pass

        def sendto(self, data, addr):
            sent.append((data, addr))

        def close(self):
            pass

    monkeypatch.setattr(socket, 'socket', FakeSocket)
    msg = wake.wake_on_lan(None, '01:02:03:04:05:06')
    assert msg == 'Woke up the computer at 01:02:03:04:05:06'
    assert sent == [(b'\xff' * 6 + bytes(range(1, 7)) * 16, ('<broadcast>', 9))]
