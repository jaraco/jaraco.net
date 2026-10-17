from jaraco.net.http.htmldir import htmldir


def test_htmldir(tmp_path):
    tmp_path.joinpath('sub').mkdir()
    tmp_path.joinpath('file.txt').write_text('hello', encoding='utf-8')
    html = htmldir(path=str(tmp_path))
    assert '<title>Directory listing for: http:///</title>' in html
    assert 'sub/</a>' in html
    assert 'size: 5">file.txt</a>' in html
