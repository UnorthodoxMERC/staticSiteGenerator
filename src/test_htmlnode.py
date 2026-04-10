import unittest 

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_one_prop(self):
        node = HTMLNode('p', 'some value', None, {'href': 'https://wwww.boot.dev'})
        self.assertEqual(node.props_to_html(), ' href="https://wwww.boot.dev"') 

    def test_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_mult_props(self):
        node = HTMLNode(None, None, None, {'href': 'https://wwww.boot.dev', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), ' href="https://wwww.boot.dev" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_to_html_pTag(self):
        node = LeafNode("p", "some value")
        self.assertEqual(node.to_html(), '<p>some value</p>')

    def test_to_html_with_props(self):
        node = LeafNode("a", "some value", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">some value</a>')

    def test_none_tag(self):
        node = LeafNode(None, 'some value')
        self.assertEqual(node.to_html(), 'some value')

    def test_none_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_mult_children(self):
        child_node = LeafNode('p', 'some value')
        child_node2 = LeafNode('p', 'some value')
        parent_node = ParentNode('div', [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), '<div><p>some value</p><p>some value</p></div>')

    def test_to_html_no_children(self):
        node = ParentNode('p', None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()