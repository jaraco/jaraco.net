import requests

from jaraco.net.http.cookies import ShelvedCookieJar, Shelf


def test_cookie_shelved(requests_mock, tmp_path):
    requests_mock.get('/', cookies={'foo': 'bar'})
    session = requests.Session()
    cookies = tmp_path / 'cookies.json'
    shelf = Shelf(cookies)
    session.cookies = ShelvedCookieJar(shelf)
    session.get('http://any/')
    assert session.cookies

    assert ShelvedCookieJar(Shelf(cookies))
