import unittest

from tghtml import unTag, transformTag, clearTag, tghtml
from bs4 import BeautifulSoup

html = "<p>ban</p>"

class TestTgHTML(unittest.TestCase):
    def test_tghtml(self):
        text = tghtml(html)
        self.assertEqual(text, "ban\n")

    def test_untag(self):
        text = unTag(html, "p")
        self.assertEqual(text, "ban")

    def test_transformtag(self):
        text = transformTag(html, "p", "span")
        self.assertEqual(text, "<span>ban</span>")

    def test_cleartag(self):
        text = clearTag("<p style='color: ban;'>ban</p>")
        self.assertEqual(text, "ban")




        
