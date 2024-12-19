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

# r"(?<!!) \[([^\[\[]*)\] \(([^\(\)]*\)"
# r"(?<!!) \[([^\[\]]*)\] \(([^\(\)]*)\)"