import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def testinit(self):
        node = HTMLNode("h1", "Hello world", None, {"href": "bootdev"})
        node2 = HTMLNode("p", "Hello There", node)
        self.assertEqual(node2.children, node)
        self.assertNotEqual(node, node2)
        self.assertEqual(node.children, None)


    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello world!")
        node2 = LeafNode("l", "Free Porn", {"href": "boot.dev"})
        node3 = LeafNode("b", "Hello world!")
        self.assertEqual(node.to_html(), "<p>Hello world!</p>")
        self.assertEqual(node2.to_html(), '<l href="boot.dev">Free Porn</l>')
        self.assertNotEqual(node, node3)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("mid", "Whatever")
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("mom", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        self.assertEqual(parent_node2.to_html(), "<mom><span>child</span><mid>Whatever</mid></mom>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("f", "niece")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = ParentNode("huh", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        parent_node2 = ParentNode("dad", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        self.assertEqual(parent_node2.to_html(), "<dad><span><b>grandchild</b></span><huh><b>grandchild</b><f>niece</f></huh></dad>")

if __name__ == "__main__":
    unittest.main()