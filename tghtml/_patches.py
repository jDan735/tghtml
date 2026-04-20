from typing_extensions import override
from dataclasses import dataclass
from selectolax.lexbor import (
    LexborHTMLParser,
    LexborNode,
)


from ._tags import I, B, Br, Code


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
    blocklist: tuple[str]

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
        return Code(el.css_first("mi").inner_html)


class FixLists(ReplacePatch):
    SELECTOR = "ul li"

    @override
    def iterate(self, el: LexborNode):
        return "■ " + el.inner_html + "END098"
