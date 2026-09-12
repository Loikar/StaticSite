import unittest
from textnode import TextType, BlockType, TextNode, text_node_to_html_node, block_to_block_type
from htmlnode import HTMLNode, LeafNode
from split import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        match2 = extract_markdown_images("This link has ![Porn](boot.dev) and ![More Porn](google.com)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        self.assertListEqual([("Porn", "boot.dev"), ("More Porn", "google.com")], match2)

    def test_extract_markdown_links(self):
        match1 = extract_markdown_links("This text leads to [Porn](boot.dev)")
        match2 = extract_markdown_links("Here is [Some Porn](what.ever) and here is [Infinite Porn!](google.com)")
        self.assertListEqual([("Porn", "boot.dev")], match1)
        self.assertListEqual([("Some Porn", "what.ever"), ("Infinite Porn!", "google.com")], match2)

    def test_split_image(self):
        node1 = TextNode("Who thought ![This](fucked.up) was a good idea?", TextType.TEXT)
        node2 = TextNode("Here are ![Some](level.shitty) ![More](level.worse)", TextType.TEXT)
        node3 = TextNode("![First](comment) on a video", TextType.TEXT)
        split1 = split_nodes_image([node1])
        split2 = split_nodes_image([node1, node2])
        split3 = split_nodes_image([node3])
        self.assertEqual(split1[2], TextNode(" was a good idea?", TextType.TEXT))
        self.assertEqual(split2[4], TextNode("Some", TextType.IMAGE, "level.shitty"))
        self.assertEqual(split3[0], TextNode("First", TextType.IMAGE, "comment"))

    def test_split_link(self):
        node1 = TextNode("Who thought [This](fucked.up) was a good idea?", TextType.TEXT)
        node2 = TextNode("Here are [Some](level.shitty) [More](level.worse)", TextType.TEXT)
        node3 = TextNode("[First](comment) on a video", TextType.TEXT)
        split1 = split_nodes_link([node1])
        split2 = split_nodes_link([node1, node2])
        split3 = split_nodes_link([node3])
        self.assertEqual(split1[2], TextNode(" was a good idea?", TextType.TEXT))
        self.assertEqual(split2[4], TextNode("Some", TextType.LINK, "level.shitty"))
        self.assertEqual(split3[0], TextNode("First", TextType.LINK, "comment"))

    def test_text_to_nodes(self):
        split1 = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        split2 = text_to_textnodes("_What kind_ of **trouble** can I get into looking at ![Porn](boot.dev)")
        self.assertEqual(split1, [
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
        ])
        self.assertEqual(split2, [
            TextNode("What kind", TextType.ITALIC),
            TextNode(" of ", TextType.TEXT),
            TextNode("trouble", TextType.BOLD),
            TextNode(" can I get into looking at ", TextType.TEXT),
            TextNode("Porn", TextType.IMAGE, "boot.dev")
        ])

    def test_markdown_split(self):
        mark1 = """
This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        mark2 = """
What's _wrong_ about enjoying some [Porn](boot.dev)?


I have the best ![ideas](level.shitty) don't you think?
"""
        blocks1 = markdown_to_blocks(mark1)
        blocks2 = markdown_to_blocks(mark2)
        self.assertEqual(blocks1, ["This is a **bolded** paragraph", "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", "- This is a list\n- with items"])
        self.assertEqual(blocks2, ["What's _wrong_ about enjoying some [Porn](boot.dev)?", "I have the best ![ideas](level.shitty) don't you think?"])


    def test_block_type(self):
        block1 = "### heading with\nrandom crap"
        block2 = """
```
Here is some
code text ```
"""
        block3 = """
> "Alas, poor yorick"
> "Who cares, let's find some porn!"
"""
        block4 = """
1. Porn
2. _Dicks_
3. Food
"""
        block5 = """
- meh
- w/e
- ugh
"""
        block6 = "Just some normal text"
        self.assertEqual(block_to_block_type(block1.strip()), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block2.strip()), BlockType.CODE)
        self.assertEqual(block_to_block_type(block3.strip()), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block4.strip()), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block5.strip()), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(block6.strip()), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()