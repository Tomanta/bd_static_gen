from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value = None, props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise ValueError("Invalid TextType")

def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
    print(text_node)

if __name__ == "__main__":
    main()