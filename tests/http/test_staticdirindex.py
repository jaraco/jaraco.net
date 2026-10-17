import pytest

from jaraco.net.http.staticdirindex import staticdirindex


def test_relative_root():
    with pytest.raises(ValueError, match='is not an absolute path'):
        staticdirindex(
            '', 'static', root='rel', match='^/nomatch', indexlister=lambda **kw: ''
        )
