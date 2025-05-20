import os
import shutil
from gen_page import generate_pages_recursively

def get_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
def copy_static(src_path, dest_path):
    root = get_root()
    src = os.path.join(root, src_path)
    dest = os.path.join(root, dest_path)
    
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted existing directory: {dest}")
        
    copy_recursive(src, dest)
    
def copy_recursive(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
        print(f"Created directory: {dest}")
        
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied file: {src_path} -> {dest_path}")
        else:
            copy_recursive(src_path, dest_path)
        

def main():
    copy_static("static", "public")
    generate_pages_recursively("content", "template.html", "public")


if __name__ == "__main__":
    main()
