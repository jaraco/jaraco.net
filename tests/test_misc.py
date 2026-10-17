import datetime
import logging
import socket
import sys
import types
import urllib.request

import pytest

from jaraco.net import icmp, importer, ntp, rss, scanner, stats, tail, tcp


def test_monitor_hosts(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def ping(host):
        raise {'a': TimeoutError(), 'b': OSError('unreachable')}[host]

    def stop(seconds):
        raise KeyboardInterrupt()

    monkeypatch.setattr(icmp, 'ping', ping)
    monkeypatch.setattr(icmp.time, 'sleep', stop)
    monkeypatch.setattr(sys, 'argv', ['monitor', 'a', 'b'])
    icmp.monitor_cmd()
    lines = (tmp_path / 'ping-results.txt').read_text(encoding='utf-8').splitlines()
    assert lines[0].endswith('host: a, res: None')
    assert lines[1].endswith('host: b, res: unreachable')


def test_url_importer(monkeypatch):
    code = b'value = 42\n'

    def urlopen(req):
        url = getattr(req, 'full_url', req)
        if 'missing' in url:
            raise OSError('not found')
        return types.SimpleNamespace(read=lambda: code)

    monkeypatch.setattr(urllib.request, 'urlopen', urlopen)
    monkeypatch.delitem(sys.modules, 'remote_mod', raising=False)
    url_importer = importer.URLImporter('http://example.com/')
    assert url_importer.find_module('missing') is None
    module = url_importer.find_module('remote_mod').load_module('remote_mod')
    assert module.value == 42


def test_ntp_command_line(monkeypatch, caplog):
    monkeypatch.setattr(ntp, 'query', lambda server, ipv6: 0)
    monkeypatch.setattr(ntp.jaraco.logging, 'setup', lambda args: None)
    handlers = [logging.NullHandler(), *logging.root.handlers]
    monkeypatch.setattr(logging.root, 'handlers', handlers)
    monkeypatch.setattr(sys, 'argv', ['ntp', 'pool.ntp.org'])
    with caplog.at_level(logging.INFO):
        ntp.handle_command_line()
    assert str(datetime.datetime.fromtimestamp(0)) in caplog.text


def test_parse_filter():
    entry = types.SimpleNamespace(updated_parsed=(2024, 1, 2, 0, 0, 0))
    assert rss.parse_filter('after 2024-01-01')(entry)
    assert not rss.parse_filter('BEFORE 2024-01-01')(entry)


def test_get_hosts_unrecognized():
    with pytest.raises(ValueError, match='Could not recognize host spec'):
        scanner.get_hosts('1:2')


def test_stats_reader(tmp_path):
    path = tmp_path / 'ping-results.txt'
    path.write_text('time: 2024-01-01 00:00:00, host: a, res: None\n', encoding='utf-8')
    reader = stats.Reader(path)
    (result,) = reader.get_stats()
    assert result.type == 'loss'


def test_tailed_file(tmp_path):
    path = tmp_path / 'log.txt'
    path.write_text('line\n', encoding='utf-8')
    tailed = tail.TailedFile(path)
    assert tailed.next() == 'line\n'
    tailed.close()


def test_tcp_connect(monkeypatch, capsys):
    class FakeSocket:
        def __init__(self, *args):
            pass

        def connect(self, addr):
            pass

    monkeypatch.setattr(socket, 'socket', FakeSocket)
    monkeypatch.setattr(sys, 'argv', ['connect', '-h', '127.0.0.1', '-p', '80'])
    tcp.test_connect()
    assert 'Successfully connected to 127.0.0.1 on port 80' in capsys.readouterr().out


def test_ntp_query(monkeypatch):
    seconds = 0x83AA7E80 + 86400
    reply = bytes(40) + seconds.to_bytes(4, 'big') + bytes(4)

    class FakeSocket:
        def __init__(self, **kwargs):
            pass

        def settimeout(self, timeout):
            pass

        def sendto(self, data, addr):
            pass

        def recvfrom(self, size):
            return reply, ('192.0.2.1', 123)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            pass

    addr_info = [(socket.AF_INET, socket.SOCK_DGRAM, 17, '', ('192.0.2.1', 123))]
    monkeypatch.setattr(socket, 'getaddrinfo', lambda *args: addr_info)
    monkeypatch.setattr(socket, 'socket', FakeSocket)
    expected = datetime.datetime.fromtimestamp(86400 + 0x83AA7E80) - datetime.timedelta(
        seconds=0x83AA7E80
    )
    assert ntp.query('pool.ntp.org') == int(expected.timestamp())
