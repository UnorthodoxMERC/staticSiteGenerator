import unittest 

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()