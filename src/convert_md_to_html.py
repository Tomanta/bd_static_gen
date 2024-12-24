import os
from markdownblocks import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith("# "):
            return line[2:]
    
    raise ValueError("Markdown has no h1")
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as md_file:
        markdown = md_file.read()

    title = extract_title(markdown)

    with open(template_path, "r") as template_file:
        template = template_file.read()
    
    new_template = template.replace('{{ Title }}', title)

    html_nodes = markdown_to_html_node(markdown)
    content = html_nodes.to_html()
    new_template = new_template.replace('{{ Content }}', content)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, "w") as dest_file:
        dest_file.write(new_template)
    
    # use markdown_to_html_node and .to_html() method to convert markdown into html
    # write the new, full HTML page into dest_path
    return