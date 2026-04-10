import unittest 

from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()