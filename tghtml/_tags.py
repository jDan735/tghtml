from selectolax.lexbor import parse_fragment, LexborNode, create_tag
from functools import partial


def Tag(tag_name: str, content: str | None) -> LexborNode:
    return parse_fragment(f"<{tag_name}>{content}</{tag_name}>")[0]


I = partial(Tag, "i")
B = partial(Tag, "b")
Br = create_tag("br")
Code = partial(Tag, "code")
