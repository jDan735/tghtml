import contextlib
from dataclasses import dataclass
from readability import Document

from bs4 import BeautifulSoup, Tag


def get_tag_content(tag: Tag) -> str:
    return "".join([i.decode() if type(i) is Tag else i for i in tag.contents])


ALLOWED_TAGS = [
    "b",
    "strong",
    "i",
    "em",
    "code",
    "s",
    "strike",
    "del",
    "u",
    "pre",
]


@dataclass
class TgHTML:
    html: str
    blocklist: list | tuple = ()
    is_wikipedia: bool = True
    enable_preprocess: bool = False

    def __post_init__(self):
        self.html: str = self.html.replace("\n", "")

        if self.enable_preprocess:
            self.html = Document(self.html).summary()

        self.soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

    def __repr__(self) -> str:
        return self.parsed

    def __str__(self) -> str:
        return self.parsed

    @property
    def parsed(self):
        self._filter()
        self._clean()
        return self.html.strip().replace("\n", "\n\n")

    def _filter(self):
        for p in self.soup.findAll("p"):
            if "Это статья о" in p.text:
                p.replace_with("")

            elif p.text.replace("\n", "") == "":
                p.replace_with("")

        for math in self.soup.find_all(class_="mwe-math-element"):
            math.replace_with(
                BeautifulSoup(
                    "<code>"
                    + math.span.math.semantics.mrow.mstyle.get_text()
                    .replace("\n", "")
                    .replace(" ", "")
                    + "</code>",
                    "html.parser",
                )
            )

        with contextlib.suppress(Exception):
            for tag in self.soup.findAll("sup", class_="reference"):
                tag.a.replace_with("")

        with contextlib.suppress(Exception):
            for tag in self.soup.findAll("span", class_="noprint"):
                tag.sup.a.replace_with("")

        for selector in self.blocklist:
            if not isinstance(selector, str):
                raise AttributeError("Use css selector instead of dict with params")

            for tag in self.soup.select(selector):
                tag.extract()

        for template in self.soup.findAll(class_="template"):
            template.replace_with("")

        if self.is_wikipedia:
            with contextlib.suppress(Exception):
                for tag in self.soup.findAll("spam", class_="no-wikidata"):
                    for _ in tag.findAll("li"):
                        tag.replace_with("")

                for tag in self.soup.find_all("ol", class_="references"):
                    tag.replace_with("")

            for tag in self.soup.find_all("span"):
                if (
                    getattr(tag, "attrs", {})
                    or {}
                    .get("style", "")
                    .strip()
                    .replace(" ", "")
                    .find("font-style:italic")
                    != -1
                ):
                    tag.name = "i"

        for tag in self.soup.find_all("a"):
            tag.replace_with(tag.text)

        for tag in self.soup.find_all("li"):
            tag.replace_with(
                BeautifulSoup(f"<p>• {get_tag_content(tag)}</p>", "html.parser")
            )

        for tag in self.soup.find_all(["q", "blockquote"]):
            tag.replace_with(
                BeautifulSoup(
                    f"<p><i>«\n   {get_tag_content(tag)}\n»</i></p>", "html.parser"
                )
            )

        for tag in self.soup.find_all(["h1"]):
            tag.replace_with(BeautifulSoup(f"<p><b>{get_tag_content(tag).upper()}</b></p>", "html.parser"))

        for tag in self.soup.find_all(["h2"]):
            tag.replace_with(BeautifulSoup(f"<p><b>{get_tag_content(tag)}</b></p>", "html.parser"))

        self.html = str(self.soup)

    def _clean(self):
        p = "".join(get_tag_content(tag) + "\n" for tag in self.soup.find_all("p"))

        soup = BeautifulSoup(p, "html.parser")
        self.html = str(self.clear_tag(soup))

    def clear_tag(self, soup: BeautifulSoup):
        for tag in soup():
            for attribute in [*tag.attrs]:
                del tag[attribute]

            if tag.name not in ALLOWED_TAGS:
                tag.replace_with("")

        return str(soup)
