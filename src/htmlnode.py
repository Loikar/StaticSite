class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        props = ""
        for key in self.props.keys():
            props += f' {key}="{self.props[key]}"'
        return props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Valueless Leaf")
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props_to_html()})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tagless Parent")
        elif not self.children:
            raise ValueError("Childless Parent")
        else:
            result = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                result += child.to_html()
            return f"{result}</{self.tag}>"