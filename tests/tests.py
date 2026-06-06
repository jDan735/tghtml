import unittest
from pathlib import Path

from haitch import a, b, code, h2, i, li, p, span, ul

from tghtml import TgHTML

HTML_PATH = Path("tests") / Path("html_examples")


class TestStringMethods(unittest.TestCase):
    def test_is_working(self):
        self.assertHTML(
            p(i("abc")),
            i("abc"),
        )

    def test_is_able_to_unpack_paragraphs(self):
        self.assertHTML(
            p(i("test")),
            i("test"),
        )

    def test_is_all_rights_with_headers(self):
        self.assertHTML(
            p(h2("Header 2")),
            b("Header 2"),
        )

    def test_proper_italic_when_it_in_style(self):
        self.assertHTML(
            p(span("Italic Text", style="font-face: italic;")),
            i("Italic Text"),
        )

    def test_check_proper_links_logic(self):
        self.assertHTML(a("test", href="ping"), "test")
        self.assertHTML(ul(li(a("test", href="abo"))), "■ test")

    def test_big_text(self):
        actual = TgHTML((HTML_PATH / "llvm-wikipedia.html").read_text())
        expected = """<b>LLVM</b> is a set of compiler and toolchain technologies that can be used to develop a frontend for any programming language and a backend for any instruction set architecture. LLVM is designed around a language-independent intermediate representation (IR) that serves as a portable, high-level assembly language that can be optimized with a variety of transformations over multiple passes. The name <i>LLVM</i> originally stood for <i>Low Level Virtual Machine.</i> However, the project has since expanded, and the name is no longer an acronym but an orphan initialism.""".strip()

        self.assertEqual(
            str(actual).split("\n\n")[0],
            expected.split("\n\n")[0],
        )

    def test_complex_text(self):
        self.assertHTML(
            (HTML_PATH / "test-page-from-ru-wikipedia.html").read_text(),
            "<b>test</b> — UNIX-утилита для проверки типа файла и сравнения значений. Возвращает код возврата 0 (ложь) или 1 (истина) в зависимости вычисления выражения <code>expr</code>. Выражения могут быть как унарными, так и бинарными. Унарные выражения часто используются для проверки статуса файла. Также допустимо сравнение чисел и строк.\n\nНачиная с UNIX System III утилита стала встроенной, также появилась вторая её форма - [.",
        )

    def test_mediawiki_math_parsing(self):
        self.assertHTML(
            r"""<span class="mwe-math-element mwe-math-element-inline"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML" alttext="{\displaystyle a}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>a</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle a}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/ffd2487510aa438433a2579450ab2b3d557e5edc" class="mwe-math-fallback-image-inline mw-invert skin-invert" aria-hidden="true" style="vertical-align: -0.338ex; width:1.23ex; height:1.676ex;" alt="{\displaystyle a}"></span>""",
            code("a"),
        )

    def test_lists(self):
        self.assertHTML(
            ul(li("Rule must be followed"), li("And another list element")),
            "■ Rule must be followed\n■ And another list element",
        )

    def test_spaces_in_pages(self):
        self.assertHTML(
            (HTML_PATH / "enwiki-Fad Gadget.html").read_text(),
            """
<b>Francis John Tovey</b> (8 September 1956 – 3 April 2002), known also by his stage name <b>Fad Gadget</b>, was a British avant-garde electronic musician and vocalist. He was a proponent of both new wave and early industrial music, fusing pop-structured songs with mechanised experimentation.

As Fad Gadget, his music was characterised by the use of synthesizers in conjunction with sounds of found objects, including drills and electric razors. His bleak, sarcastic and darkly humorous lyrics were filled with biting social commentary toward subjects such as machinery, industrialisation, consumerism, human sexuality, mass media, religion, domestic violence and dehumanization, often sung in a deadpan voice.    
        """.strip(),
        )

    def test_metadata_hidden(self):
        self.assertHTML(
            (HTML_PATH / "enwiki-Transcarpathian-referendum.html").read_text(),
            """
<b>1 декабря 1991 года</b> в один день с всеукраинским референдумом и первыми выборами президента Украины состоялся <b>Закарпатский общеобластной референдум</b>. На референдум был вынесен вопрос «О предоставлении Закарпатской области статуса автономного края в составе Украины».

Ещё до вхождения в состав СССР 30 января 1946 года Подкарпатская Русь (историческое название края) являлась республикой, с автономным статусом, в составе Чехословакии, в соответствии с конституционным законом 326\\1938, от 22 ноября 1938.
""".strip(),
        )

    def test_math_pages_are_correct(self):
        self.assertHTMLfile(
            "pi.html",
            """
<code>π</code>, <b>π</b> (произносится «<b>пи</b>»)&nbsp;— математическая постоянная, равная отношению длины окружности к её диаметру. Числу «пи» также можно дать множество других определений, например это отношение полупериода функции <code>y=sin(x)</code> к её максимальному значению. Обозначается буквой греческого алфавита «π». На декабрь 2025 года известны первые 314 триллионов (или 3,14*1014) знаков числа «пи» после запятой.""",
        )

    def assertStr(self, first, second):
        self.assertEqual(first.__str__(), second.__str__().strip())

    def assertHTML(self, first, second):
        self.assertStr(TgHTML(first), second)

    def assertHTMLfile(self, file: str, second):
        self.assertHTML((HTML_PATH / file).read_text(), second)
