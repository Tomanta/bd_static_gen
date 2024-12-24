class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""

        prop_list = []
        for key, value in self.props.items():
            prop_list.append(f'{key}="{value}"')
        
        return " " + " ".join(prop_list).strip()
    
    def __repr__(self):
        return(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")
    
    def __eq__(self, html_node):
        return (
            self.tag == html_node.tag
            and self.value == html_node.value
            and self.children == html_node.children
            and self.props == html_node.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
            super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("value is required")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return(f"LeafNode({self.tag}, {self.value}, {self.props})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("ParentNode requires tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode requires children")

        child_html = [child.to_html() for child in self.children]
        return f"<{self.tag}>{''.join(child_html)}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"