import re
from textnode import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) ->list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or delimiter not in old_node.text:
            new_list.append(old_node)
        else:
            text = old_node.text
            while delimiter in text:
                split = text.split(delimiter, maxsplit=2)
                if len(split) != 3:
                    raise Exception("Invalid markdown syntax")
                new_list.append(TextNode(split[0], TextType.TEXT))
                new_list.append(TextNode(split[1], text_type))
                text = split[2]
            new_list.append(TextNode(text, TextType.TEXT))
    return new_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) ->list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
        else:
            text = node.text
            for i in range(0, len(matches)):
                sections = text.split(f"![{matches[i][0]}]({matches[i][1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
                text = sections[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) ->list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
        else:
            text = node.text
            for i in range(0, len(matches)):
                sections = text.split(f"[{matches[i][0]}]({matches[i][1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))
                text = sections[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    result = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    return split_nodes_link(result)

def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    blocks = []
    for i in sections:
        if i:
            blocks.append(i.strip())
    return blocks