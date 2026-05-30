import unittest

from textnode import TextNode, TextType


class TestTextType(unittest.TestCase):
    def test_value_is_str(self):
        self.assertTrue(TextType.BOLD.value == "bold")

    def test_no_match_str(self):
        self.assertFalse(TextType.ITALIC == "italic")


class TestTextNode(unittest.TestCase):
    def test_str_text_type_rejected(self):
        with self.assertRaises(TypeError) as cm:
            TextNode("This is a text node", "bold")  # pyright: ignore[reportArgumentType]
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


if __name__ == "__main__":
    unittest.main()
