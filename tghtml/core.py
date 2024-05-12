import re

from dataclasses import dataclass, field
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
    "blockquote",
]


@dataclass
class TgHTML:
    html: str
    blocklist: list | tuple = ()
    is_wikipedia: bool = True
    enable_preprocess: bool = True
    allowed_tags: list = field(default_factory=lambda: ALLOWED_TAGS)

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

        return (
            re.sub("\n{2,}", "\n", self.html.strip().replace("\ufeff", "\n"))
            .replace("JDAN_EXTRA_SPACE", "\n")
            .replace("\n", "\n\n")
        )

    def _filter(self):
        for p in self.soup.findAll("p"):
            if "Это статья о" in p.text or "Vide etiam paginam discretivam:" in p.text:
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

        try:
            for tag in self.soup.findAll("sup", class_="reference"):
                tag.a.replace_with("")

            for tag in self.soup.findAll("span", class_="noprint"):
                tag.sup.a.replace_with("")
        except Exception:
            pass

        for item in self.blocklist:
            if type(item) == str:
                x = item.split(".")

                if len(x) > 1:
                    item = [x[0] or "div", {"class": x[1]}]
                else:
                    item = [item]

            for tag in self.soup.findAll(*item):
                tag.replace_with("")

        if self.is_wikipedia:
            try:
                for tag in self.soup.findAll("spam", class_="no-wikidata"):
                    for _ in tag.findAll("li"):
                        tag.replace_with("")

                for tag in self.soup.find_all("ol", class_="references"):
                    tag.replace_with("")
            except Exception:
                pass

            for tag in self.soup.find_all("span"):
                if (
                    getattr(tag, "attrs", {})
                    or {}.get("style", "")
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
                BeautifulSoup("<p>• " + get_tag_content(tag) + "</p>", "html.parser")
            )

        for tag in self.soup.find_all(["h2"]):
            tag.replace_with(
                BeautifulSoup(
                    "<p><b>" + get_tag_content(tag) + "</b></p>", "html.parser"
                )
            )

        for tag in self.soup.find_all(["cite"]):
            tag.replace_with(
                BeautifulSoup(" <i>" + get_tag_content(tag) + "</i>", "html.parser")
            )

        for tag in self.soup.find_all("div", {"class": "ts-Цитата"}):
            child = tag.find("blockquote")
            new_tag = BeautifulSoup(
                TgHTML(get_tag_content(child), allowed_tags=["b", "i"]).parsed,
                "html.parser",
            )

            tag.replace_with(new_tag)

        for tag in self.soup.find_all("blockquote"):
            tag.wrap(Tag(name="p"))

        for tag in self.soup.find_all(["h1"]):
            tag.replace_with(
                BeautifulSoup(
                    "<p><b>" + get_tag_content(tag).upper() + "</b></p>", "html.parser"
                )
            )

        for tag in self.soup.find_all(["h2"]):
            tag.replace_with(
                BeautifulSoup(
                    "<p><b>" + get_tag_content(tag) + "</b></p>", "html.parser"
                )
            )

        self.html = str(self.soup)

    def _clean(self):
        p = "".join(get_tag_content(tag) + "\n" for tag in self.soup.find_all("p"))

        soup = BeautifulSoup(p, "html.parser")
        self.html = str(self.clear_tag(soup))

    def clear_tag(self, soup: BeautifulSoup):
        for tag in soup():
            for attribute in [*tag.attrs]:
                del tag[attribute]

            if tag.name not in self.allowed_tags:
                tag.replace_with("")

        return str(soup)
