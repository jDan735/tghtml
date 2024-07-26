from tghtml.core import TgHTML


with open("test.html", encoding="UTF-8") as f:
    t = TgHTML(f.read()).parsed
    print(t)
