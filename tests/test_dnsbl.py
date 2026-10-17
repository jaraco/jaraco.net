import socket

from jaraco.net import dnsbl


def test_lookup(monkeypatch):
    def gethostbyname(name):
        return {'example.com': '1.2.3.4'}.get(name, '127.0.0.2')

    monkeypatch.setattr(socket, 'gethostbyname', gethostbyname)
    hit = dnsbl.Service('bl.example').lookup('example.com')
    assert str(hit) == 'example.com listed with bl.example as 127.0.0.2'
