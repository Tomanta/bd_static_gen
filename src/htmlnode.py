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
        
        return " ".join(prop_list).strip()
    
    def __repr__(self):
        return(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
            super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("value is required")
        if self.tag is None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"
