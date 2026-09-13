import unittest
from htmlnode import *
from textnode import *
from split import *
from convert import *

class TestConvert(unittest.TestCase):
    def test_convert(self):
        paragraph = """
This is a **bolded** paragraph
text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(paragraph)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
        multi = """
### Here's a **Bold Headline**

A short article paragraph of _important_ text

- Various
- Items
- List

1. A
2. Numbered
3. List
"""
        node2 = markdown_to_html_node(multi)
        html2 = node2.to_html()
        self.assertEqual(html2, "<div><h3>Here's a <b>Bold Headline</b></h3><p>A short article paragraph of <i>important</i> text</p><ul><li>- Various</li><li>- Items</li><li>- List</li></ul><ol><li>1. A</li><li>2. Numbered</li><li>3. List</li></ol></div>")
        quotes = """
> "Alas, poor yorick"
> "Who cares, let's find some porn!"
"""
        node3 = markdown_to_html_node(quotes)
        html3 = node3.to_html()
        self.assertEqual(html3, '<div><blockquote>> "Alas, poor yorick"\n> "Who cares, let\'s find some porn!"</blockquote></div>')
        code = """
```
Here is some
code text ```
"""
        node4 = markdown_to_html_node(code)
        html4 = node4.to_html()
        self.assertEqual(html4, "<div><pre><code>Here is some\ncode text </code></pre></div>")