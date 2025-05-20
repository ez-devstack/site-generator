import os
from pathlib import Path
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 title found")

def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()
        
    with open(template_path, "r") as f:
        template = f.read()
        
    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()
    
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{base_path}')
    full_html = full_html.replace('src="/', f'src="{base_path}')

    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)
        
def generate_pages_recursively(dir_path_content, template_path, des_dir_path, base_path="/"):
    for entry in os.listdir(dir_path_content):
        src_entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(des_dir_path, entry)
        
        if os.path.isfile(src_entry_path) and src_entry_path.endswith(".md"):
            dest_html_path = os.path.splitext(dest_entry_path)[0] + ".html"
            generate_page(src_entry_path, template_path, dest_html_path, base_path)
        
        if os.path.isdir(src_entry_path):
            generate_pages_recursively(src_entry_path, template_path, dest_entry_path, base_path)
            