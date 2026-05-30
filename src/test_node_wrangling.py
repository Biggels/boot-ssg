import unittest

from htmlnode import LeafNode
from node_wrangling import text_node_to_html_node
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
