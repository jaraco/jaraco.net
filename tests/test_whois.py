from importlib_resources import files


def test_bolivia_handler():
    from jaraco.net.whois import BoliviaWhoisHandler

    handler = BoliviaWhoisHandler('microsoft.com.bo')
    handler.client_address = '127.0.0.1'
    saved_resp = files('tests') / 'nic.bo.html'
    handler._response = saved_resp.read_bytes()
    result = handler.ParseResponse()
    assert 'Microsoft Corporation' in result
