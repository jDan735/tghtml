import unittest

from tghtml import TgHTML, untag
from bs4 import BeautifulSoup

HTML = "<p>ban</p>"

class TestTgHTML(unittest.TestCase):
    def test_TgHTML(self):
        tghtml = TgHTML(HTML)
        self.assertEqual(tghtml.parsed, "ban\n")

    def test_untag(self):
        text = untag(HTML, "p")
        self.assertEqual(text, "ban")
