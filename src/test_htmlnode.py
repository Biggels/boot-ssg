import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_no_props(self):
        node = HTMLNode(tag="p", value="this is a paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props(self):
        node = HTMLNode(tag="p", value="this is a paragraph", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_one_prop(self):
        node = HTMLNode(
            tag="a",
            value="zing to bing",
            props={"href": "https://www.bing.com"},
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.bing.com"')

    def test_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="moogle to google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode(
            tag="a",
            value="moogle to google",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag=a, value=moogle to google, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})",
        )
