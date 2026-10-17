import socket
from typing import ClassVar

from jaraco.net import udp


class FakeSocket:
    instances: ClassVar[list['FakeSocket']] = []
    errors: ClassVar[list[BaseException]] = []

    def __init__(self, *args):
        self.sent = []
        self.instances.append(self)

    def settimeout(self, timeout):
        pass

    def bind(self, addr):
        pass

    def connect(self, addr):
        self.addr = addr

    def send(self, data):
        self.sent.append(data)

    def recvfrom(self, size):
        raise self.errors.pop(0)

    def close(self):
        pass


def test_sender(monkeypatch):
    monkeypatch.setattr(FakeSocket, 'instances', [])
    monkeypatch.setattr(socket, 'socket', FakeSocket)
    monkeypatch.setattr('sys.argv', ['send', '-c', '127.0.0.1:9999', '-m', 'hi'])
    sender = udp.Sender()
    (sock,) = FakeSocket.instances
    assert sock.sent == [b'hi']
    assert sock.addr == ('127.0.0.1', 9999)
    assert repr(sender) == "message sent to ('127.0.0.1', 9999)"


def test_echo_server(monkeypatch):
    monkeypatch.setattr(FakeSocket, 'instances', [])
    monkeypatch.setattr(FakeSocket, 'errors', [TimeoutError(), KeyboardInterrupt()])
    monkeypatch.setattr(socket, 'socket', FakeSocket)
    monkeypatch.setattr('sys.argv', ['echo', '-p', '9999'])
    udp.EchoServer()
