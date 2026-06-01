import unittest

from htmlnode import LeafNode
from node_wrangling import split_nodes_delimiter, text_node_to_html_node
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
    # test delim at beginning and end
    # test empty list

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
