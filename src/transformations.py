import re

from blocktype import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
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
                # matched_text is guaranteed present right now because it's rebuilt from the extractor
                # but if the extractor pattern changes in the future this could break
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
                # matched_text is guaranteed present right now because it's rebuilt from the extractor
                # but if the extractor pattern changes in the future this could break
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


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = split_nodes_image([TextNode(text, TextType.PLAIN)])
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [block.strip() for block in markdown.split("\n\n")]
    blocks = [block for block in blocks if block]
    return blocks


def block_to_block_type(block: str) -> BlockType:
    # empty strings should be paragraphs
    # if we don't guard here, the all() on quote will match the empty
    if not block:
        return BlockType.PARAGRAPH

    # HEADING
    # the negated set could also just be ., because . doesn't include newline by default
    # but the negated set is more explicit
    if re.match(r"^#{1,6} [^\n]+$", block):
        return BlockType.HEADING

    # CODE
    if re.match(
        r"^```\n.*```$", block, re.DOTALL
    ):  # the DOTALL flag makes . include newline
        return BlockType.CODE

    # QUOTE
    if all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE

    # UNORDERED_LIST
    if all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST

    # ORDERED_LIST
    if all(
        line.startswith(f"{count}. ")
        for count, line in enumerate(block.splitlines(), start=1)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return html_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    if markdown is None:
        raise TypeError("markdown must be a string")

    blocks = markdown_to_blocks(markdown)

    if not blocks:
        return ParentNode(tag="div", children=[LeafNode(tag=None, value="")])

    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                # we don't use whitespace to organize html
                block = block.replace("\n", " ")
                block_children = text_to_children(block)
                block_node = ParentNode(tag="p", children=block_children)
            case BlockType.HEADING:
                match = re.match(r"^#{1,6} ", block)
                if not match:
                    raise ValueError(
                        "something has gone wrong, because a blocktype of heading should definitely start with some number of #"
                    )
                heading_prefix = match.group()
                heading_prefix_end = match.end()
                heading_level = heading_prefix.count("#")
                block = block[heading_prefix_end:]
                block_children = text_to_children(block)
                block_node = ParentNode(
                    tag=f"h{heading_level}", children=block_children
                )
            case BlockType.CODE:
                # worth noting this is dependent on the exact definition of a code block from block_to_block_type
                # i.e. we're not allowing ```python at the start of a code block, so we can safely cut off the first 4 (```\n)
                # but if that changes, this will break
                block = block[4:-3]
                block_child = LeafNode(tag="code", value=block)
                block_node = ParentNode(tag="pre", children=[block_child])
            case BlockType.QUOTE:
                block = " ".join(
                    line.lstrip(">").strip() for line in block.splitlines()
                )
                block_children = text_to_children(block)
                block_node = ParentNode(tag="blockquote", children=block_children)
            case BlockType.UNORDERED_LIST:
                li_nodes = []
                for li in block.splitlines():
                    li = li[2:]
                    li_children = text_to_children(li)
                    li_node = ParentNode(tag="li", children=li_children)
                    li_nodes.append(li_node)
                block_node = ParentNode(tag="ul", children=li_nodes)
            case BlockType.ORDERED_LIST:
                li_nodes = []
                for li in block.splitlines():
                    li = li.split(". ", 1)[1]
                    li_children = text_to_children(li)
                    li_node = ParentNode(tag="li", children=li_children)
                    li_nodes.append(li_node)
                block_node = ParentNode(tag="ol", children=li_nodes)

        block_nodes.append(block_node)

    return ParentNode("div", children=block_nodes)
