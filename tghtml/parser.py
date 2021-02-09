import re

from bs4 import BeautifulSoup


def unTag(tag, tag_name):
    return tag.replace(f"<{tag_name}>", "") \
              .replace(f"</{tag_name}>", "")


def transformTag(html, tag_old, tag_new):
    return html.replace(f"<{tag_old}>", f"<{tag_new}>") \
               .replace(f"</{tag_old}>", f"</{tag_new}>")


def clearTag(soup):
    if soup.__class__.__name__ != "BeautifulSoup":
        soup = BeautifulSoup(soup, "lxml")

    for tag in soup():
        for attribute in [*tag.attrs]:
            try:
                del tag[attribute]
            except Exception:
                pass

    allowedTags = ["b", "strong", "i", "em", "code", "s",
                   "strike", "del", "u", "pre"]

    page = str(soup)

    page = re.sub(r"\[.{0,}?\]", "", page)

    page = page.replace("<img/>", "") \
               .replace("<br/>", "") \
               .replace("<br>", "")
    page = unTag(page, "p")

    for tag in soup():
        if not (tag.name in allowedTags):
            page = unTag(page, tag.name)

    return page


def tghtml(page, tagBlocklist=[["ol", {"class": "references"}]]):
    for tag in "ul", "ol":
        page = transformTag(page, tag, "p")

    page = page.replace("<li>", "• ") \
               .replace("</li>", "")

    soup = BeautifulSoup(page, "lxml")

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
        p = ""

        for tag in soup.findAll("p"):
            tag = BeautifulSoup(str(tag), "lxml")
            p += unTag(str(clearTag(tag)), "p") + "\n"

        soup = BeautifulSoup(p, "lxml")
        page = str(clearTag(soup))

        return page

    except Exception as e:
        print(e)
        return "Не удалось распарсить"
