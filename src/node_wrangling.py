from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": "https://www.google.com"}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={
                    "src": text_node.url,
                    "alt": text_node.text,
                },
            )
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN or delimiter not in node.text:
            new_nodes.append(node)
        else:
            chunks = node.text.split(delimiter)
            # if it split into an even number of chunks, that means there was an odd number of delims
            # which means a mismatched opener/closer
            if len(chunks) % 2 == 0:
                raise ValueError("One of old_nodes contains invalid Markdown syntax")
            for i, chunk in enumerate(chunks):
                # if it starts or ends with a delim, split makes empty strings, which we don't need to pass through
                # we still want to iterate over them to preserve the even-odd ordering
                if chunk == "":
                    continue
                # the chunks will always start with a plain one, then alternate, so evens are plain
                if i % 2 == 0:
                    new_nodes.append(TextNode(chunk, TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(chunk, text_type))
    return new_nodes
