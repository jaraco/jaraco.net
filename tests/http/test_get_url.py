import email.message
import os
import urllib.request

import pytest

from jaraco.net.http import get_url


class FakeResponse(list):
    def __init__(self, lines, **headers):
        super().__init__(lines)
        self.headers = email.message.Message()
        for name, value in headers.items():
            self.headers[name.replace('_', '-')] = value


def test_get_url_local_newer(tmp_path, monkeypatch):
    """
    When the local file is newer and the same size, just touch it.
    """
    resp = FakeResponse(
        [b'data'],
        last_modified='Mon, 01 Jan 2024 00:00:00 GMT',
        content_length='4',
    )
    monkeypatch.setattr(urllib.request, 'urlopen', lambda url: resp)
    target = tmp_path / 'file.dat'
    target.write_bytes(b'data')
    assert get_url('http://example.com/file.dat', dest=target) is None
    assert os.path.getmtime(target) == 1704067200


def test_get_url_exists(tmp_path, monkeypatch):
    resp = FakeResponse(
        [b'data'],
        last_modified='Mon, 01 Jan 2024 00:00:00 GMT',
        content_length='4',
    )
    monkeypatch.setattr(urllib.request, 'urlopen', lambda url: resp)
    target = tmp_path / 'file.dat'
    target.write_bytes(b'data')
    with pytest.raises(RuntimeError, match='exists'):
        get_url(
            'http://example.com/file.dat',
            dest=target,
            replace_newer=False,
            touch_older=False,
        )


def test_get_url_download(tmp_path, monkeypatch):
    resp = FakeResponse([b'da', b'ta'], content_length='4')
    monkeypatch.setattr(urllib.request, 'urlopen', lambda url: resp)
    target = tmp_path / 'file.dat'
    assert str(get_url('http://example.com/file.dat', dest=target)) == str(target)
    assert target.read_bytes() == b'data'
