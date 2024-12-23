import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
        
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = []
            sections = node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, section not closed")
            for n in range(len(sections)):
                if sections[n] == "": # empty, doesn't need a new node
                    continue 
                if n % 2 == 0: # These should just be text
                    split_nodes.append(TextNode(sections[n], TextType.TEXT))
                else: # These are the formatted
                    split_nodes.append(TextNode(sections[n], text_type))
            new_nodes.extend(split_nodes)
    
    return new_nodes

def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_pattern, text)

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT: # Not a text node
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)

        if len(images) == 0: # empty, no processing
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text

        for image in images:
            split_text = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            remaining_text = split_text[1]
        
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:

        if old_node.text_type != TextType.TEXT: # Not a text node
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        
        if len(links) == 0: # empty, no processing
            new_nodes.append(old_node)
            continue
        
        remaining_text = old_node.text
        for link in links:
            split_text = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, url=link[1]))
            remaining_text = split_text[1]
        
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes


