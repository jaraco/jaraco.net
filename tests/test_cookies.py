import requests

from jaraco.net.http.cookies import ShelvedCookieJar, FlushableShelf


def test_cookie_shelved(requests_mock, tmp_path, check_concurrent_dbm):
    requests_mock.get('/', cookies={'foo': 'bar'})
    session = requests.Session()
    cookies = tmp_path / 'cookies'
    shelf = FlushableShelf(cookies)
    session.cookies = ShelvedCookieJar(shelf)
    session.get('http://any/')
    assert session.cookies

    assert ShelvedCookieJar(FlushableShelf(cookies))
