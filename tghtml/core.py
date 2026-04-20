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
]


@dataclass(frozen=True)
class TgHTML:
    source_html: Any
    blocklist: list[str] = field(default_factory=lambda: DEFAULT_BLOCKLIST)
    filtered: str = field(init=False, default="")
    parsed: str = field(init=False, default="")

    def __post_init__(self):
        sel = LexborHTMLParser(self.source_html.__str__()).css_first("body")

        for patch in sum(
            map(
                lambda x: x.__subclasses__(),
                Patch.__subclasses__(),
            ),
            [],
        ):
            if patch == BlocklistPatch:
                BlocklistPatch(sel=sel, blocklist=self.blocklist)
                continue

            patch(sel)

        res = sel.css_first("body").inner_html
        parsed = (
            clean(
                (res or "").replace("<br>", "\n"),
                tags=ALLOWED_TAGS,
            )
            .replace("\n", "\n\n")
            .strip()
        )

        object.__setattr__(
            self,
            "parsed",
            re.sub(r"\n{3,}", r"\n\n", parsed)
            .replace("END098■", "\n■")
            .replace("END098", ""),
        )

    def __str__(self):
        return self.parsed

    def __eq__(a, b):
        return a.__str__() == b.__str__().strip()
