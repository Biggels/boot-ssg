import unittest

from htmlnode import LeafNode
from node_wrangling import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
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
            url="https://www.google.com",
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


class TestSplitNodesImage(unittest.TestCase):
    def test_empty_list_returns_empty_list(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_single_image_in_middle_splits_into_three_nodes(self):
        node = TextNode("see ![a cat](a.png) here", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("see ", TextType.PLAIN),
                TextNode("a cat", TextType.IMAGE, "a.png"),
                TextNode(" here", TextType.PLAIN),
            ],
        )

    def test_multiple_images_all_converted(self):
        node = TextNode("![a](1.png) and ![b](2.png)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("a", TextType.IMAGE, "1.png"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("b", TextType.IMAGE, "2.png"),
            ],
        )

    def test_image_at_start_has_no_leading_empty_node(self):
        node = TextNode("![first](a.png) then text", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("first", TextType.IMAGE, "a.png"),
                TextNode(" then text", TextType.PLAIN),
            ],
        )

    def test_image_at_end_has_no_trailing_empty_node(self):
        node = TextNode("text then ![last](z.png)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("text then ", TextType.PLAIN),
                TextNode("last", TextType.IMAGE, "z.png"),
            ],
        )

    def test_node_that_is_entirely_one_image_yields_only_that_node(self):
        # Nothing surrounds the image, so there should be no empty PLAIN nodes
        # on either side -- just the single IMAGE node.
        node = TextNode("![solo](a.png)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("solo", TextType.IMAGE, "a.png")],
        )

    def test_plain_node_with_no_markdown_passes_through_unchanged(self):
        node = TextNode("just some plain prose", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("just some plain prose", TextType.PLAIN)],
        )

    def test_multiple_input_nodes_flattened_in_order(self):
        nodes = [
            TextNode("text with ![a](1.png) image", TextType.PLAIN),
            TextNode("more ![b](2.png) here", TextType.PLAIN),
        ]
        self.assertEqual(
            split_nodes_image(nodes),
            [
                TextNode("text with ", TextType.PLAIN),
                TextNode("a", TextType.IMAGE, "1.png"),
                TextNode(" image", TextType.PLAIN),
                TextNode("more ", TextType.PLAIN),
                TextNode("b", TextType.IMAGE, "2.png"),
                TextNode(" here", TextType.PLAIN),
            ],
        )

    def test_non_plain_node_passed_through_unchanged(self):
        # A node that is already a non-PLAIN type (e.g. from an earlier pass in
        # the chain) is not re-parsed; it is appended as-is.
        node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("already bold", TextType.BOLD)],
        )

    def test_malformed_image_left_as_plain_text(self):
        node = TextNode("this has a broken ![image](url and stuff", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("this has a broken ![image](url and stuff", TextType.PLAIN)],
        )

    def test_nested_image_converts_only_inner_image(self):
        # Only the well-formed inner image is converted; the broken outer
        # wrapper is left behind as literal PLAIN text.
        node = TextNode(
            "![a cool picture![my best friend](i.imgur.com/abcd)](i.imgur.com/efgh)",
            TextType.PLAIN,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("![a cool picture", TextType.PLAIN),
                TextNode("my best friend", TextType.IMAGE, "i.imgur.com/abcd"),
                TextNode("](i.imgur.com/efgh)", TextType.PLAIN),
            ],
        )

    def test_image_with_empty_url_left_as_plain_text(self):
        # An image with no url is not converted -- fail soft and leave the
        # literal markdown in place rather than producing a urlless IMAGE node.
        node = TextNode("see ![alt]() here", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("see ![alt]() here", TextType.PLAIN)],
        )

    def test_image_with_empty_alt_uses_empty_string_alt(self):
        # Missing alt text is fine: the image still renders, alt="" is valid.
        node = TextNode("see ![](a.png) here", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("see ", TextType.PLAIN),
                TextNode("", TextType.IMAGE, "a.png"),
                TextNode(" here", TextType.PLAIN),
            ],
        )

    def test_duplicate_identical_images_both_converted(self):
        node = TextNode("![cat](a.png) and again ![cat](a.png)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("cat", TextType.IMAGE, "a.png"),
                TextNode(" and again ", TextType.PLAIN),
                TextNode("cat", TextType.IMAGE, "a.png"),
            ],
        )

    def test_image_splitter_ignores_links(self):
        # The image splitter must leave link syntax untouched in the PLAIN text.
        node = TextNode("![img](a.png) and [link](b.com)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("img", TextType.IMAGE, "a.png"),
                TextNode(" and [link](b.com)", TextType.PLAIN),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_empty_list_returns_empty_list(self):
        self.assertEqual(split_nodes_link([]), [])

    def test_single_link_in_middle_splits_into_three_nodes(self):
        node = TextNode("see [a site](a.com) here", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("see ", TextType.PLAIN),
                TextNode("a site", TextType.LINK, "a.com"),
                TextNode(" here", TextType.PLAIN),
            ],
        )

    def test_multiple_links_all_converted(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_link_at_start_has_no_leading_empty_node(self):
        node = TextNode("[first](a.com) then text", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("first", TextType.LINK, "a.com"),
                TextNode(" then text", TextType.PLAIN),
            ],
        )

    def test_link_at_end_has_no_trailing_empty_node(self):
        node = TextNode("text then [last](z.com)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("text then ", TextType.PLAIN),
                TextNode("last", TextType.LINK, "z.com"),
            ],
        )

    def test_node_that_is_entirely_one_link_yields_only_that_node(self):
        # Nothing surrounds the link, so there should be no empty PLAIN nodes
        # on either side -- just the single LINK node.
        node = TextNode("[solo](a.com)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("solo", TextType.LINK, "a.com")],
        )

    def test_plain_node_with_no_markdown_passes_through_unchanged(self):
        node = TextNode("just some plain prose", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("just some plain prose", TextType.PLAIN)],
        )

    def test_multiple_input_nodes_flattened_in_order(self):
        nodes = [
            TextNode("text with [a](1.com) link", TextType.PLAIN),
            TextNode("more [b](2.com) here", TextType.PLAIN),
        ]
        self.assertEqual(
            split_nodes_link(nodes),
            [
                TextNode("text with ", TextType.PLAIN),
                TextNode("a", TextType.LINK, "1.com"),
                TextNode(" link", TextType.PLAIN),
                TextNode("more ", TextType.PLAIN),
                TextNode("b", TextType.LINK, "2.com"),
                TextNode(" here", TextType.PLAIN),
            ],
        )

    def test_non_plain_node_passed_through_unchanged(self):
        # A node that is already a non-PLAIN type (e.g. from an earlier pass in
        # the chain) is not re-parsed; it is appended as-is.
        node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("already bold", TextType.BOLD)],
        )

    def test_malformed_link_left_as_plain_text(self):
        node = TextNode("this has a broken [link](url and stuff", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("this has a broken [link](url and stuff", TextType.PLAIN)],
        )

    def test_nested_link_converts_only_inner_link(self):
        # Only the well-formed inner link is converted; the broken outer
        # wrapper is left behind as literal PLAIN text.
        node = TextNode(
            "[ok](a.com) and [outer[inner](u1)](u2)",
            TextType.PLAIN,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("ok", TextType.LINK, "a.com"),
                TextNode(" and [outer", TextType.PLAIN),
                TextNode("inner", TextType.LINK, "u1"),
                TextNode("](u2)", TextType.PLAIN),
            ],
        )

    def test_link_with_empty_url_left_as_plain_text(self):
        # A link with no url is not converted -- fail soft and leave the literal
        # markdown in place rather than producing a urlless LINK node.
        node = TextNode("see [text]() here", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("see [text]() here", TextType.PLAIN)],
        )

    def test_link_with_empty_text_falls_back_to_url(self):
        # An empty <a> is invisible/unclickable, so we use the url as the
        # visible link text to keep the link usable.
        node = TextNode("see [](b.com) here", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("see ", TextType.PLAIN),
                TextNode("b.com", TextType.LINK, "b.com"),
                TextNode(" here", TextType.PLAIN),
            ],
        )

    def test_duplicate_identical_links_both_converted(self):
        node = TextNode("[cat](a.com) and again [cat](a.com)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("cat", TextType.LINK, "a.com"),
                TextNode(" and again ", TextType.PLAIN),
                TextNode("cat", TextType.LINK, "a.com"),
            ],
        )

    def test_link_splitter_ignores_images(self):
        # The link splitter must not be fooled by the [..](..) shape inside an
        # image; only the real link is converted.
        node = TextNode("![img](a.png) and [link](b.com)", TextType.PLAIN)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("![img](a.png) and ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "b.com"),
            ],
        )
