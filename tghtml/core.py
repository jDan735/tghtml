import re

from bs4 import BeautifulSoup


class TgHTML:
    ALLOWED_TAGS = ["b", "strong", "i", "em", "code", "s",
                    "strike", "del", "u", "pre"]

    def __init__(self, html, blocklist=(), is_wikipedia=True):
        self.blocklist = blocklist
        self.html = html
        self.is_wikipedia = is_wikipedia
        self.soup = BeautifulSoup(self.html, "lxml")

    def __repr__(self):
        return self.parsed

    def __str__(self):
        return self.parsed

    @property
    def parsed(self):
        self._filter()
        self._clean()
        return self.html

    def _filter(self):
        for p in self.soup.findAll("p"):
            if "Это статья об" in p.text:
                p.replace_with("")

            elif p.text.replace("\n", "") == "":
                p.replace_with("")

        for item in self.blocklist:
            for tag in self.soup.findAll(*item):
                tag.replace_with("")

        for tag in "ul", "ol":
            self.html = untag(self.html, tag)

        if self.is_wikipedia:
            try:
                for tag in self.soup.findAll("spam", class_="no-wikidata"):
                    for li in tag.findAll("li"):
                        tag.replace_with("")
            except Exception:
                pass

        self.html = str(self.soup)
        with open("test.txt", "w", encoding="UTF-8") as f:
            f.write(self.html)

        self.replace(["<li>", "<p>• "],
                     ["</li>", "</p>"])

    def _clean(self):
        p = ""

        for tag in self.soup.findAll("p"):
            tag = BeautifulSoup(str(tag), "lxml")
            p += untag(str(self._clear_tag(tag)), "p") + "\n"

        soup = BeautifulSoup(p, "lxml")
        self.html = str(self._clear_tag(soup))

    def replace(self, *args):
        for arg in args:
            self.html = self.html.replace(*arg)

    def _replace_tag(self, tag, new_tag="p"):
        tag, new_tag = Tag(tag), Tag(new_tag)

        self.replace([tag.start, new_tag.end],
                     [tag.end, new_tag.end])

    def _clear_tag(self, soup):
        if soup.__class__.__name__ != "BeautifulSoup":
            soup = BeautifulSoup(soup, "lxml")

        for tag in soup():
            for attribute in [*tag.attrs]:
                try:
                    del tag[attribute]
                except Exception:
                    pass

        html = str(soup)
        html = re.sub(r"\[.{0,}?\]", "", html)

        self.replace(["<img/>", ""],
                     ["<br/>", ""],
                     ["<br>", ""])

        html = untag(html, "p")

        for tag in self.soup():
            if not (tag.name in self.ALLOWED_TAGS):
                html = untag(html, tag.name)

        return html


def untag(tag, tag_name):
    return tag.replace(f"<{tag_name}>", "") \
              .replace(f"</{tag_name}>", "")


class Tag:
    def __init__(self, tag_name, text=""):
        self.start = f"<{tag_name}>"
        self.end = f"</{tag_name}>"
        self.name = tag_name
        self.text = self.start + text + self.end


if __name__ == "__main__":
    print(TgHTML("a"))
