from textnode import TextNode, TextType
from htmlnode import LeafNode

import os
import shutil

def clean_folder_if_exists(path):
    if os.path.exists(path):
        print(f"DEBUG: Removing files from {path}")
        shutil.rmtree(path)

def copy_folder(source, destination):
    if not os.path.exists(source):
        raise Exception(f"DEBUG: Source path does not exist! {source}, {destination}")
    
    clean_folder_if_exists(destination)
    os.mkdir(destination)
    for item in os.listdir(source):
        if os.path.isfile(os.path.join(source, item)):
            shutil.copy(os.path.join(source, item), destination)
        else:
            copy_folder(os.path.join(source, item), os.path.join(destination, item))

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
    static_root = './static'
    public_root = './public'
    copy_folder(static_root, public_root)

if __name__ == "__main__":
    main()