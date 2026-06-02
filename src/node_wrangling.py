import re

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
                tag="a", value=text_node.text, props={"href": text_node.url}
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


def extract_markdown_images(text: str | None) -> list[tuple]:
    # md img format is ![alt text](url)
    # !\[(.*?)\]\((.*?)\) was rejected because it breaks with nested brackets/parens
    if not text:
        return []
    matches = re.findall(pattern=r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", string=text)
    return matches


def extract_markdown_links(text: str | None) -> list[tuple]:
    # md link format is [display text](url)
    # (?<!!)\[(.*?)\]\((.*?)\) was rejected because it breaks with nested brackets/parens
    if not text:
        return []
    matches = re.findall(pattern=r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", string=text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
        else:
            text = node.text
            matches = extract_markdown_images(text)
            for alt_text, src_url in matches:
                if src_url == "":
                    continue
                matched_text = f"![{alt_text}]({src_url})"
                pre, text = text.split(matched_text, maxsplit=1)
                if pre != "":
                    new_nodes.append(TextNode(pre, TextType.PLAIN))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, src_url))
            if text != "":
                new_nodes.append(TextNode(text, TextType.PLAIN))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
        else:
            text = node.text
            matches = extract_markdown_links(text)
            for display_text, href_url in matches:
                if href_url == "":
                    continue
                matched_text = f"[{display_text}]({href_url})"
                pre, text = text.split(matched_text, maxsplit=1)
                if pre != "":
                    new_nodes.append(TextNode(pre, TextType.PLAIN))
                if display_text == "":
                    display_text = href_url
                new_nodes.append(TextNode(display_text, TextType.LINK, href_url))
            if text != "":
                new_nodes.append(TextNode(text, TextType.PLAIN))

    return new_nodes
