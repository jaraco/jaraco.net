import datetime
import io
import socket

from jaraco.net.http import servers


class FakeConn:
    def __init__(self, request, fail_send=False):
        self.request = request
        self.fail_send = fail_send
        self.sent = []

    def settimeout(self, timeout):
        pass

    def recv(self, size):
        data, self.request = self.request[:size], self.request[size:]
        return data

    def send(self, data):
        if self.fail_send:
            raise OSError('connection reset')
        self.sent.append(data)

    def close(self):
        pass


def make_server(cls=servers.Simple):
    return cls('', 0, 1, datetime.timedelta(), io.StringIO())


def test_get_content_length():
    headers = 'GET / HTTP/1.0\r\ncontent-length: 12\r\n'
    assert servers.Simple.get_content_length(headers) == 12


def test_get_response_error(capsys):
    server = make_server()
    server.conn = FakeConn(b'POST / HTTP/1.0\r\n\r\n', fail_send=True)
    server.get_response()
    assert 'Error connection reset' in capsys.readouterr().out


def test_serve_until_auth(monkeypatch):
    conn = FakeConn(b'GET / HTTP/1.0\r\nAuthorization: Basic Zm9v\r\n\r\n')

    class FakeSocket:
        def __init__(self, *args):
            pass

        def bind(self, addr):
            pass

        def listen(self, backlog):
            pass

        def accept(self):
            return conn, ('127.0.0.1', 12345)

    monkeypatch.setattr(socket, 'socket', FakeSocket)
    make_server(servers.AuthRequest).serve()
    assert conn.sent[-1] == b'\r\nYou are authenticated as Basic Zm9v'
