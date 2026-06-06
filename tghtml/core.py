import re
from dataclasses import dataclass, field
from typing import Any

from nh3 import clean
from selectolax.lexbor import LexborHTMLParser

from ._patches import BlocklistPatch, Patch

ALLOWED_TAGS = {
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
}

DEFAULT_BLOCKLIST = [
    "ol.references",
    ".reference",
    "table",
    "tdclass",
    ".infobox-label",
    "td",
    "figure",
    "div.metadata",
    ".noprint",
    ".floatright",
    ".error",
]


@dataclass(frozen=True)
class TgHTML:
    source_html: Any
    blocklist: list[str] = field(default_factory=lambda: DEFAULT_BLOCKLIST)
    enable_preprocess: bool = False
    filtered: str = field(init=False, default="")
    parsed: str = field(init=False, default="")

    def __post_init__(self):
        blocklist = set(self.blocklist + DEFAULT_BLOCKLIST)
        sel = LexborHTMLParser(self.source_html.__str__()).css_first("body")

        for patch in sum(
            map(
                lambda x: x.__subclasses__(),
                Patch.__subclasses__(),
            ),
            [],
        ):
            if patch == BlocklistPatch:
                BlocklistPatch(sel=sel, blocklist=blocklist)
                continue

            patch(sel)

        res = sel.css_first("body").inner_html
        parsed = clean(
            (res or "").replace("<br>", "\n"),
            tags=ALLOWED_TAGS,
        )

        object.__setattr__(self, "parsed", self.remove_spaces(parsed))

    def remove_spaces(self, text: str) -> str:
        _ = text.replace("\n", "\n\n").strip()
        _ = re.sub(r" *\n *", "\n", _)
        _ = re.sub(r"\n{3,}", r"\n\n", _)
        _ = re.sub(" {2,}", " ", _)
        return _.replace("END098■", "\n■").replace("END098", "")

    def __str__(self):
        return self.parsed

    def __eq__(a, b):
        return a.__str__() == b.__str__().strip()
