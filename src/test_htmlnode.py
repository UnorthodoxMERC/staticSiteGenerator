import unittest 

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_tag(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node, node2)

    def test_value(self):
        node = HTMLNode('h1', 'some value')
        node2 = HTMLNode('h1', 'some value')
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()