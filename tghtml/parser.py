from bs4 import BeautifulSoup


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
                              "id", "dir", "lang", "rel"]:
                try:
                    del tag[attribute]
                except Exception:
                    pass

        return str(soup).replace("<p>", "") \
                        .replace("<a>", "") \
                        .replace("<span>", "") \
                        .replace("</p>", "") \
                        .replace("</a>", "") \
                        .replace("</span>", "")

    except Exception as e:
        print(e)
        return "Не удалось распарсить"
