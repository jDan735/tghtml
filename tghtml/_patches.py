from dataclasses import dataclass

from pylatexenc.latex2text import LatexNodes2Text
from selectolax.lexbor import (
    LexborHTMLParser,
    LexborNode,
)
from typing_extensions import override

from ._tags import B, Br, Code, I


latex = LatexNodes2Text()


def get_node(html: str):
    return LexborHTMLParser(html).css_first("body")


@dataclass
class Patch:
    sel: LexborNode | LexborHTMLParser


class SimplePatch(Patch): ...


@dataclass
class ReplacePatch(Patch):
    SELECTOR = ""

    def __post_init__(self):
        for el in self.sel.css(self.SELECTOR):
            el.replace_with(self.iterate(el))

    def iterate(self, el: LexborNode):
        raise NotImplementedError


########## EXAMPLES ###########


@dataclass
class FixItalicPatch(SimplePatch):
    def __post_init__(self):
        for el in self.sel.css("span[style='font-face: italic;']"):
            el.replace_with(I(el.inner_html))


@dataclass
class AddSpaceToParagraphsPatch(SimplePatch):
    def __post_init__(self):
        for el in self.sel.css("p"):
            el.insert_after(Br)


@dataclass
class BlocklistPatch(ReplacePatch):
    blocklist: list[str]

    @property
    def SELECTOR(self) -> str:
        return ", ".join(self.blocklist)

    def iterate(self, el: LexborNode):
        return ""


class FixItalicSimplePatch(ReplacePatch):
    SELECTOR = "span[style='font-face: italic;']"

    @override
    def iterate(self, el: LexborNode):
        return I(el.inner_html)


class FixH2Patch(ReplacePatch):
    SELECTOR = "h2"

    @override
    def iterate(self, el: LexborNode):
        return B(el.inner_html)


class MathPatch(ReplacePatch):
    SELECTOR = "span.mwe-math-element"

    @override
    def iterate(self, el: LexborNode):
        return Code(
            latex.latex_to_text(
                (el.css_first("annotation").inner_html or "").replace(
                    r"\tfrac", r"\frac"
                )
            )
        )


class FixLists(ReplacePatch):
    SELECTOR = "ul li"

    @override
    def iterate(self, el: LexborNode):
        return get_node("■ " + el.inner_html + "END098")
