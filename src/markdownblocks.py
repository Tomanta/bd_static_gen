from enum import Enum
from htmlnode import ParentNode,LeafNode
from textnode import TextType
from inline_markdown import text_to_textnodes
import re

def text_to_children(markdown_text):
    text_nodes = text_to_textnodes(markdown_text)
    child_nodes = []
    for text_node in text_nodes:
        match text_node.text_type:
            case TextType.TEXT:
                new_child = LeafNode('p', text_node.text)
            case _:
                raise NotImplementedError
        child_nodes.append(new_child)
    return child_nodes

def block_to_html(markdown):
    blocks = markdown_to_blocks(markdown) # Create blocks
    # For each block, determine the type
    # Based on the type, create a new HTMLNode
    # Assign proper child node
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "paragraph":
            children.extend(text_to_children(block))
    
    return ParentNode('div',children=children)

def markdown_to_blocks(text):
    blocks = text.split('\n\n')
    clean_list = [x.strip() for x in blocks if x != ""]
    return clean_list

def is_header_block(block):
    return block.startswith(("#", "##", "###", "####", "#####", "######"))

def is_code_block(block):
    # This may be incorrect, course says must be more than 1 line and uses lines[0].startwith('```') and lines[-1].startswith('```')
    return len(block.split("```")) == 3

def is_quote_block(block):
    lines = block.split("\n")

    for line in lines:
        if not line.startswith(">"):
            return False
    
    return True

def is_ordered_list_block(block):
    lines = block.split("\n")

    current_counter = 1
    for line in lines:
        if not line.startswith(f"{current_counter}. "):
            return False
        current_counter += 1

    return True


def is_unordered_list_block(block):
    lines = block.split("\n")

    for line in lines:
        if not line.startswith(('* ', '- ')):
            return False

    return True

def block_to_block_type(block):
    if is_header_block(block):
        return "heading"
    if is_code_block(block):
        return "code"
    if is_quote_block(block):
        return "quote"
    if is_unordered_list_block(block):
        return "unordered_list"
    if is_ordered_list_block(block):
        return "ordered_list"

    return "paragraph"

