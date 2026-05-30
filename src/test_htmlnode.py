import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_to_html_value_is_none(self):
        node = LeafNode(tag="p", value=None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_tag_is_none(self):
        node = LeafNode(tag=None, value="this is some untagged text")
        self.assertEqual(node.to_html(), "this is some untagged text")

    def test_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_repr(self):
        node = LeafNode(tag="p", value="this is a paragraph")
        self.assertEqual(
            node.__repr__(), "LeafNode(tag=p, value=this is a paragraph, props=None)"
        )


class TestParentNode(unittest.TestCase):
    # no tag, empty tag
    # props, no props
    # no children, empty children
    # one child, two children
    # one child w/ one grandchild, two children w/ two grandchildren
    # child with props
    # child and grandchild w/ props

    def test_props_default(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertIsNone(parent_node.props)

    def test_to_html_none_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            tag=None, children=[child_node], props={"href": "https://www.google.com"}
        )
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_empty_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            tag="", children=[child_node], props={"href": "https://www.google.com"}
        )
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_none_children(self):
        parent_node = ParentNode("div", children=None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_empty_children(self):
        parent_node = ParentNode("div", children=[])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node_2 = LeafNode("span", "also a child")
        parent_node = ParentNode("div", [child_node, child_node_2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><span>also a child</span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_child_with_props(self):
        child_node = LeafNode("a", "click me", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://www.google.com">click me</a></div>',
        )
