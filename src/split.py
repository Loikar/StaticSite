from textnode import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) ->list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT or delimiter not in old_node.text:
            new_list.append(old_node)
        else:
            split = old_node.text.split(delimiter, maxsplit=2)
            if len(split) != 3:
                raise Exception("Invalid markdown syntax")
            split[0] = TextNode(split[0], TextType.TEXT)
            split[1] = TextNode(split[1], text_type)
            split[2] = TextNode(split[2], TextType.TEXT)
            for i in range(0, len(split)):
                if split[i].text:
                    new_list.append(split[i])
    return new_list
