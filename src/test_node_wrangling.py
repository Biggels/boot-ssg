import unittest

from htmlnode import LeafNode
from node_wrangling import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    text_node_to_html_node,
)
from textnode import TextNode, TextType


class TestNodeConversion(unittest.TestCase):
    def test_plain(self):
        node = TextNode(text="This is a plain text node", text_type=TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a plain text node")
        self.assertIsNone(html_node.props)

    def test_bold(self):
        node = TextNode(text="This is a bold text node", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode(text="This is an italic text node", text_type=TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode(text="This is a code text node", text_type=TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode(
            text="This is a link text node",
            text_type=TextType.LINK,
            url="htts://www.google.com",
        )
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode(
            text="This is a really cool image",
            text_type=TextType.IMAGE,
            url="htts://www.coolimages.com/really-cool-image",
        )
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "htts://www.coolimages.com/really-cool-image",
                "alt": "This is a really cool image",
            },
        )


class TestSplitNodes(unittest.TestCase):
    def test_split_empty_list(self):
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_split_no_delims(self):
        node = TextNode("This is text with no inline markdown", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with no inline markdown", TextType.PLAIN),
            ],
        )

    def test_split_wrong_delim(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with a **bolded phrase** in the middle",
                    TextType.PLAIN,
                )
            ],
        )

    def test_split_no_closing_delim(self):
        node = TextNode(
            "This is text with a **bolded phrase in the middle", TextType.PLAIN
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_non_plain(self):
        node = TextNode("this is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("this is bold text", TextType.BOLD)])

    def test_split_single_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.PLAIN),
            ],
        )

    def test_split_single_bold_start(self):
        node = TextNode("**Bold text** starts this one", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode(" starts this one", TextType.PLAIN),
            ],
        )

    def test_split_single_bold_end(self):
        node = TextNode("This one ends with **bold text**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This one ends with ", TextType.PLAIN),
                TextNode("bold text", TextType.BOLD),
            ],
        )

    def test_split_single_italic(self):
        node = TextNode(
            "This is text with an _italic phrase_ in the middle", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" in the middle", TextType.PLAIN),
            ],
        )

    def test_split_single_code(self):
        node = TextNode(
            "This is text with a `code block` in the middle", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" in the middle", TextType.PLAIN),
            ],
        )

    def test_split_multiple_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** and **another bolded phrase** and **another bolded phrase** in the middle",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("another bolded phrase", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("another bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.PLAIN),
            ],
        )

    def test_split_multiple_diff(self):
        node = TextNode(
            "This is text with a **bolded phrase** and an _italic phrase_ and a `code block` in the middle",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(
                    " and an _italic phrase_ and a `code block` in the middle",
                    TextType.PLAIN,
                ),
            ],
        )

    def test_split_multiple_nodes(self):
        old_nodes = [
            TextNode(
                "This is text with a **bolded phrase** in the middle", TextType.PLAIN
            ),
            TextNode(
                "This is text with an _italic phrase_ in the middle", TextType.PLAIN
            ),
            TextNode("This is text with a `code block` in the middle", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.PLAIN),
                TextNode(
                    "This is text with an _italic phrase_ in the middle", TextType.PLAIN
                ),
                TextNode(
                    "This is text with a `code block` in the middle", TextType.PLAIN
                ),
            ],
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_returns_all_images_in_order(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_empty_string_returns_empty_list(self):
        self.assertEqual(extract_markdown_images(""), [])

    def test_none_returns_empty_list(self):
        self.assertEqual(extract_markdown_images(None), [])

    def test_text_with_no_markdown_returns_empty_list(self):
        self.assertEqual(extract_markdown_images("just some plain text"), [])

    def test_captures_images_flush_at_start_and_end(self):
        # An image as the very first thing and an image as the very last thing
        # must both be captured fully.
        text = "![start](a.png) middle text ![end](b.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("start", "a.png"), ("end", "b.png")],
        )

    def test_ignores_malformed_or_incomplete_syntax(self):
        # None of these is a complete image structure, so nothing should match.
        for text in ["()", "[]", "()()", "[][]", "![alt]", "![alt](url"]:
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_images(text), [])

    def test_matches_image_with_empty_alt_text(self):
        self.assertEqual(
            extract_markdown_images("![](https://example.com/image.png)"),
            [("", "https://example.com/image.png")],
        )

    def test_matches_image_with_empty_url(self):
        self.assertEqual(
            extract_markdown_images("![alt text]()"),
            [("alt text", "")],
        )

    def test_matches_image_with_both_fields_empty(self):
        self.assertEqual(extract_markdown_images("![]()"), [("", "")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_returns_all_links_in_order(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_empty_string_returns_empty_list(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_none_returns_empty_list(self):
        self.assertEqual(extract_markdown_links(None), [])

    def test_text_with_no_markdown_returns_empty_list(self):
        self.assertEqual(extract_markdown_links("just some plain text"), [])

    def test_captures_links_flush_at_start_and_end(self):
        # A link as the very first thing and a link as the very last thing
        # must both be captured fully.
        text = "[start](a.com) middle text [end](b.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("start", "a.com"), ("end", "b.com")],
        )

    def test_ignores_malformed_or_incomplete_syntax(self):
        # None of these is a complete link structure, so nothing should match.
        for text in ["()", "[]", "()()", "[][]", "[text]", "[text](url"]:
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_links(text), [])

    def test_matches_link_with_empty_display_text(self):
        self.assertEqual(
            extract_markdown_links("[](https://example.com)"),
            [("", "https://example.com")],
        )

    def test_matches_link_with_empty_url(self):
        self.assertEqual(
            extract_markdown_links("[click here]()"),
            [("click here", "")],
        )

    def test_matches_link_with_both_fields_empty(self):
        self.assertEqual(extract_markdown_links("[]()"), [("", "")])


class TestImageLinkMutualExclusivity(unittest.TestCase):
    # In mixed text every span of source belongs to exactly one kind of node:
    # the image extractor sees only images, the link extractor only links, and
    # neither is fooled by the other's syntax.

    def test_image_extractor_returns_only_images_from_mixed_text(self):
        text = "![img](a.png) and [link](b.com)"
        self.assertEqual(extract_markdown_images(text), [("img", "a.png")])

    def test_link_extractor_does_not_match_link_text_inside_image(self):
        # The image ![img](a.png) contains a link-shaped [img](a.png) right
        # after the '!'. The link extractor must return only the real link.
        text = "![img](a.png) and [link](b.com)"
        self.assertEqual(extract_markdown_links(text), [("link", "b.com")])

    def test_image_extractor_returns_empty_for_link_only_text(self):
        self.assertEqual(extract_markdown_images("[link](b.com)"), [])

    def test_link_extractor_returns_empty_for_image_only_text(self):
        self.assertEqual(extract_markdown_links("![img](a.png)"), [])


class TestNestedBracketHandling(unittest.TestCase):
    # Nested inline elements are not supported. The agreed behavior is not to
    # bail out, but to extract the inner, well-formed element and ignore the
    # broken outer wrapper — so brackets/parens used inside text or url never
    # get swallowed into a match, and a clean element elsewhere still matches.

    def test_nested_image_extracts_only_inner_image(self):
        text = "![a cool picture![my best friend](i.imgur.com/abcd)](i.imgur.com/efgh)"
        self.assertEqual(
            extract_markdown_images(text),
            [("my best friend", "i.imgur.com/abcd")],
        )

    def test_clean_image_still_matched_alongside_nested_image(self):
        text = "![ok](a.png) and ![outer![inner](u1)](u2)"
        self.assertEqual(
            extract_markdown_images(text),
            [("ok", "a.png"), ("inner", "u1")],
        )

    def test_brackets_inside_link_extract_only_inner_link(self):
        text = "[a cool link[my best friend]]([www.google.com](https://www.google.com))"
        self.assertEqual(
            extract_markdown_links(text),
            [("www.google.com", "https://www.google.com")],
        )

    def test_clean_link_still_matched_alongside_nested_link(self):
        text = "[ok](a.com) and [outer[inner](u1)](u2)"
        self.assertEqual(
            extract_markdown_links(text),
            [("ok", "a.com"), ("inner", "u1")],
        )


class TestStrictBracketAndParenRule(unittest.TestCase):
    # We deliberately accept a strict rule for simplicity: a stray bracket in the
    # display/alt text, or a stray paren in the url, disqualifies that whole
    # element from matching. This drops some arguably-valid links (e.g. literal
    # brackets in display text) rather than reach for a real balancing parser,
    # which is out of scope here. These pin that we lose them on purpose.

    def test_link_with_brackets_in_display_text_does_not_match(self):
        self.assertEqual(
            extract_markdown_links("[a cool link[my best friend]](www.google.com)"),
            [],
        )

    def test_link_with_parens_in_url_does_not_match(self):
        self.assertEqual(
            extract_markdown_links("[a cool link](www.google.com(a cool site))"),
            [],
        )

    def test_image_with_stray_bracket_in_alt_text_does_not_match(self):
        self.assertEqual(
            extract_markdown_images("![a cool image[](i.imgur.com/abcd)"),
            [],
        )

    def test_invalid_image_tail_is_still_a_valid_empty_link(self):
        # The image above is rejected, but its trailing "[](url)" is itself a
        # structurally valid empty-text link, so the link extractor picks it up.
        # We accept this and lock it in rather than be surprised by it later.
        self.assertEqual(
            extract_markdown_links("![a cool image[](i.imgur.com/abcd)"),
            [("", "i.imgur.com/abcd")],
        )
