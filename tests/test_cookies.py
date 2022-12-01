import platform

import requests

from jaraco.net.http.cookies import ShelvedCookieJar, FlushableShelf


def test_cookie_shelved(requests_mock, tmp_path):
    requests_mock.get('/', cookies={'foo': 'bar'})
    session = requests.Session()
    cookies = tmp_path / 'cookies'
    shelf = FlushableShelf(cookies)
    session.cookies = ShelvedCookieJar(shelf)
    session.get('http://any/')
    assert session.cookies

    if platform.system() == "Windows":
        # need to detach original jar before a new one can connect
        shelf.close()

    assert ShelvedCookieJar(FlushableShelf(cookies))
