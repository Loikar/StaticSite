from textnode import *
from htmlnode import *
from split import *

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for node in textnodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes

def list_helper(text):
    lines = text.split("\n")
    listnodes = []
    for line in lines:
        listnodes.append(ParentNode("li", text_to_children(line)))
    return listnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    listnodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                text = block.lstrip("#")
                count = len(block) - len(text)
                listnodes.append(ParentNode(f"h{count}", text_to_children(text.strip())))
            case BlockType.CODE:
                text = block.lstrip("```\n")
                text = text.rstrip("```")
                listnodes.append(ParentNode("pre", [LeafNode("code", text)]))
            case BlockType.QUOTE:
                listnodes.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.UNORDERED_LIST:
                listnodes.append(ParentNode("ul", list_helper(block)))
            case BlockType.ORDERED_LIST:
                listnodes.append(ParentNode("ol", list_helper(block)))
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                listnodes.append(ParentNode("p", text_to_children(text)))
    return ParentNode("div", listnodes)