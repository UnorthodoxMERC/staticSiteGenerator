import unittest

from textnode import TextNode, TextType, text_node_to_html_node

from nodeSplitter import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes

from md_to_block import markdown_to_blocks


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

    def test_split_node_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("code block", TextType.CODE),
                                        TextNode(" word", TextType.TEXT),
                                    ])
        
    def test_split_node_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("bold", TextType.BOLD),
                                        TextNode(" word", TextType.TEXT),
                                    ])
        
    def test_split_node_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a ", TextType.TEXT),
                                        TextNode("italic", TextType.ITALIC),
                                        TextNode(" word", TextType.TEXT),
                                    ])
    
    def test_split_node_no_closing(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    
    def test_split_same_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_with_no_text_before(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_no_text_after(self):
        node = TextNode(
            "some text ![image](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com")
            ],
            new_nodes,
        )

    def test_split_images_with_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com")
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode(
            "some text and some more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("some text and some more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_mixed(self):
        nodes = [
            TextNode(
                "some text ![image](https://i.imgur.com)",
                TextType.TEXT,
            ),
            TextNode(
                "some text ![image](https://i.imgur.com)",
                TextType.IMAGE,
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com"),
                TextNode("some text ![image](https://i.imgur.com)", TextType.IMAGE),
            ],
            new_nodes,
        ) 
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_same_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com) and again [link](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and again ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
            ],
            new_nodes,
        )

    def test_split_link_with_no_text_before(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) some text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_with_no_text_after(self):
        node = TextNode(
            "some text [link](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com")
            ],
            new_nodes,
        )

    def test_split_link_no_link(self):
        node = TextNode(
            "some text and some more",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("some text and some more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_mixed(self):
        nodes = [
            TextNode(
                "some text [link](https://i.imgur.com)",
                TextType.TEXT,
            ),
            TextNode(
                "some text [link](https://i.imgur.com)",
                TextType.LINK,
            ),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("some text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode("some text [link](https://i.imgur.com)", TextType.LINK),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()