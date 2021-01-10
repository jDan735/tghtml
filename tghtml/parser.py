import re

from bs4 import BeautifulSoup


def unTag(tag_name, tag):
    return tag.replace(f"<{tag_name}>", "") \
              .replace(f"</{tag_name}>", "")


def tghtml(page, tagBlocklist=[]):
    soup = BeautifulSoup(page, 'lxml')

    try:
        for t in soup.findAll("p"):
            if "Это статья об" in t.text:
                t.replace_with("")

        for item in tagBlocklist:
            for tag in soup.findAll(*item):
                try:
                    tag.replace_with("")
                except Exception:
                    pass

        for tag in soup.findAll("p"):
            if tag.text.replace("\n", "") == "":
                tag.replace_with("")
    except Exception:
        pass

    try:
        soup = soup.p

        for tag in soup():
            for attribute in ["class", "title", "href", "style", "name",
                              "id", "dir", "lang", "rel", "src", "alt",
                              "height", "width"]:
                try:
                    del tag[attribute]
                except Exception:
                    pass

        allowedTags = ["b", "strong", "i", "em", "code", "s",
                       "strike", "del", "u", "pre"]

        page = str(soup)

        page = re.sub(r"\[.{0,}?\]", "", page)

        page = page.replace("<img/>", "")
        page = unTag("p", page)

        for tag in soup():
            if not (tag.name in allowedTags):
                page = unTag(tag.name, page)

        return page

    except Exception as e:
        print(e)
        return "Не удалось распарсить"
