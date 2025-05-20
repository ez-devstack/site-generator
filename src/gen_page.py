import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()
        
    with open(template_path, "r") as f:
        template = f.read()
        
    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()
    
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)