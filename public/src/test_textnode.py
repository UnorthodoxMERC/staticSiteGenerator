import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_different_text_type(self):
        node1 = TextNode('This is a text node', TextType.BOLD_TEXT)
        node2 = TextNode('This is a text node', TextType.ITALIC_TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("this is a text node", TextType.IMAGE, 'https://www.pictures.com')
        node2 = TextNode("this is a text node", TextType.IMAGE, 'https://www.pictures.com')
        self.assertEqual(node1, node2)

    def test_notEqual_url(self):
        node1 = TextNode("this is a text node", TextType.IMAGE, 'https://www.pictures.com')
        node2 = TextNode("this is a text node", TextType.IMAGE, 'https://www.images.com')
        self.assertNotEqual(node1, node2)


    def test_NoneUrl_vs_url(self):
        node1 = TextNode("this is a text node", TextType.IMAGE, 'https://www.pictures.com')
        node2 = TextNode("this is a text node", TextType.IMAGE)
        self.assertNotEqual(node1, node2)
    


if __name__ == "__main__":
    unittest.main()