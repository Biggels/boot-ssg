import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextType(unittest.TestCase):
    def test_value_is_str(self):
        self.assertTrue(TextType.BOLD.value == "bold")

    def test_no_match_str(self):
        self.assertFalse(TextType.ITALIC == "italic")


class TestTextNode(unittest.TestCase):
    def test_str_text_type_rejected(self):
        with self.assertRaises(TypeError) as cm:
            TextNode("This is a text node", "bold")
        self.assertIn("must be a TextType", str(cm.exception))

    def test_textnode_text_type_accepted(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIs(node.text_type, TextType.BOLD)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_default(self):
        node = TextNode("This is a text node", TextType.LINK, url=None)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a Text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("click me", TextType.LINK, "https://www.google.com")
        self.assertEqual(
            node.__repr__(), "TextNode(click me, link, https://www.google.com)"
        )


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


if __name__ == "__main__":
    unittest.main()
