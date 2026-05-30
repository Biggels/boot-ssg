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
