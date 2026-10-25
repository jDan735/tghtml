from selectolax.lexbor import LexborHTMLParser, LexborNode, create_tag
from functools import partial


def Tag(tag_name: str, content: str | None) -> LexborNode:
    a =  LexborHTMLParser(
        f"<{tag_name}>{content}</{tag_name}>",
        is_fragment=True
    )

    return a.root


I = partial(Tag, "i")
B = partial(Tag, "b")
Br = create_tag("br")
Code = partial(Tag, "code")
