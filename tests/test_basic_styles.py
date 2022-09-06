from tghtml import TgHTML


def test_italic_tag():
    assert TgHTML("<p><i>test</i></p>").parsed == "<i>test</i>"


def test_style_italic():
    assert (
        TgHTML("<p><span style='font-face: italic;'>Test</span></p>").parsed
        == "<i>Test</i>"
    )


def test_h1():
    assert TgHTML("<p><h1>Test</h1></p>").parsed == "<b>TEST</b>"


def test_h2():
    assert TgHTML("<p><h2>Test</h2></p>").parsed == "<b>Test</b>"


def test_blockquote():
    assert TgHTML("<p><blockquote>Test</blockquote></p>").parsed == "<i>   «Test»</i>"
