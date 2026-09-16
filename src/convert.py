import os
from textnode import *
from htmlnode import *
from split import *

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for node in textnodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes

def list_helper(text, type):
    lines = text.split("\n")
    listnodes = []
    for line in lines:
        if type == "ul":
            item = line[2:]
        elif type == "ol":
            item = line[3:]
        listnodes.append(ParentNode("li", text_to_children(item)))
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
                text = block.replace(">", "").strip()
                listnodes.append(ParentNode("blockquote", text_to_children(text)))
            case BlockType.UNORDERED_LIST:
                listnodes.append(ParentNode("ul", list_helper(block, "ul")))
            case BlockType.ORDERED_LIST:
                listnodes.append(ParentNode("ol", list_helper(block, "ol")))
            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ")
                listnodes.append(ParentNode("p", text_to_children(text)))
    return ParentNode("div", listnodes)

def extract_title(markdown: str):
    text = markdown.strip()
    if not text.startswith("# "):
        raise Exception("No h1 header")
    split = text.split("\n", maxsplit=1)
    return split[0]

def generate_page(from_path, template_path, dest_path):
    dest_file = dest_path.replace(".md", ".html")
    print(f"Generating page from {from_path} to {dest_file} using {template_path}")
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    node = markdown_to_html_node(content)
    htmlstr = node.to_html()
    title = extract_title(content)
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", htmlstr)
    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)
    with open(dest_file, "w") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for i in os.listdir(dir_path_content):
        cont = os.path.join(dir_path_content, i)
        dest = os.path.join(dest_dir_path, i)
        if os.path.isfile(cont):
            if cont.endswith(".md"):
                generate_page(cont, template_path, dest)
        else:
            if not os.path.isdir(dest):
                os.mkdir(dest)
            generate_pages_recursive(cont, template_path, dest)