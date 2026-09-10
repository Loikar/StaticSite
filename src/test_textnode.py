import unittest
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode
from split import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("Hello world", TextType.ITALIC)
        node4 = TextNode("Hello world", TextType.TEXT)
        node5 = TextNode("Hello world", TextType.TEXT, "boot.dev")
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("Whatever", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "i")
        self.assertEqual(node2.text, html_node2.value)

    def test_split(self):
        node = TextNode("_Hello_ **world**", TextType.TEXT)
        node2 = TextNode("This is a **text** node", TextType.TEXT)
        node3 = TextNode("This is **wrong*", TextType.TEXT)
        node4 = TextNode("Bold text", TextType.BOLD)
        split = split_nodes_delimiter([node], "_", TextType.ITALIC)
        split2 = split_nodes_delimiter([node, node2, node4], "**", TextType.BOLD)
        split3 = split_nodes_delimiter(split, "**", TextType.BOLD)
        self.assertEqual(split[0], TextNode("Hello", TextType.ITALIC))
        self.assertEqual(split2[0], TextNode("_Hello_ ", TextType.TEXT))
        self.assertEqual(split2[3], TextNode("text", TextType.BOLD))
        self.assertEqual(split2[5], TextNode("Bold text", TextType.BOLD))
        self.assertEqual(split3[2], TextNode("world", TextType.BOLD))

if __name__ == "__main__":
    unittest.main()