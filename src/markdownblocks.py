from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

def text_to_children(markdown_text):
    text_nodes = text_to_textnodes(markdown_text)
    child_nodes = []
    for text_node in text_nodes:
        child_nodes.append(text_node_to_html_node(text_node))
    return child_nodes

def generate_blockquote(markdown_block):
    text_nodes = []
    for line in markdown_block.split("\n"):
        text_nodes.extend(text_to_children(line[1:].strip()))
    return ParentNode('blockquote', children=text_nodes)

def generate_header(markdown_block):
    text_split = markdown_block.split(" ", 1)
    header_level = len(text_split[0])
    header_node = ParentNode(f'h{header_level}', children=text_to_children(text_split[1]))
    return header_node

def generate_unordered_list(markdown_block):
    list_nodes = []
    for line in markdown_block.split("\n"):
        list_nodes.append(ParentNode('li', children=
            text_to_children(line[2: ])
        ))
    return ParentNode("ul", children=list_nodes)

def generate_code_block(markdown):
    clean_markdown = markdown.strip("```")
    text_nodes = []
    for line in clean_markdown.split("\n"):
        text_nodes.extend(text_to_children(line))
    return ParentNode("pre",children=[ParentNode("code", children=text_nodes)])    

def generate_ordered_list(markdown):
    list_nodes = []
    for line in markdown.split("\n"):
        list_nodes.append(ParentNode('li', children=
            text_to_children(line.split(' ',1)[1])
        ))
    return ParentNode("ol", children=list_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) # Create blocks
    # For each block, determine the type
    # Based on the type, create a new HTMLNode
    # Assign proper child node
    html_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case "paragraph":
                parent = ParentNode('p',children=text_to_children(block))
            case "quote":
                parent = generate_blockquote(block)
            case "heading":
                parent = generate_header(block)
            case "code":
                parent = generate_code_block(block)
            case "unordered_list":
                parent = generate_unordered_list(block)
            case "ordered_list":
                parent = generate_ordered_list(block)
            case _:
                raise ValueError("Invalid block type")
        html_nodes.append(parent)
    
    return ParentNode('div',children=html_nodes)

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

