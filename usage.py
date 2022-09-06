from tghtml.tghtml2 import TgHTML


with open("file.html", encoding="UTF-8") as f:
    TgHTML(f.read()).parsed
