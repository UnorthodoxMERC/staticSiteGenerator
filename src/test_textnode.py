import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("test node", TextType.TEXT)
        node2 = TextNode("test node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("test node", TextType.TEXT, "www.boomer.com")
        node2 = TextNode("test node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode('This is a text node', TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, 'This is a text node')

    def test_bold(self):
        node = TextNode('this is a bold node', TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'this is a bold node')

    def test_link(self):
        node = TextNode('babam', TextType.LINK, 'https://www.babam.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'babam')
        self.assertEqual(html_node.props, {'href': 'https://www.babam.com'})

    def test_image(self):
        node = TextNode('alt text', TextType.IMAGE, 'https://www.babam.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src': 'https://www.babam.com', 'alt': 'alt text'})

    def test_wrong_TextType(self):
        node = TextNode('blah blah', 'blah')
        with self.assertRaises(ValueError):
            html_node = text_node_to_html_node(node)




if __name__ == "__main__":
    unittest.main()