import unittest
from textnode import TextType, TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()