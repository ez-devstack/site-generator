import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter not in ('**', '_', '`'):
        raise Exception("invalid Markdown syntax")
    
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split_node = node.text.split(delimiter)
        
        for i, part in enumerate(split_node):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
        
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text == "":
            continue
        
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        
        text = node.text
        for image_alt, image_link in matches:
            split_text = text.split(f"![{image_alt}]({image_link})", 1)
        
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                
            #Update text to text after image for next loop    
            text = split_text[1]
        
        #if leftover text after images, add text
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes
            

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text == "":
            continue
        
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        
        text = node.text
        for anchor, link in matches:
            split_text = text.split(f"[{anchor}]({link})", 1)
        
            if split_text[0]:
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            
            new_nodes.append(TextNode(anchor, TextType.LINK, link))
                
            #Update text to text after link for next loop    
            text = split_text[1]
        
        #if leftover text after links, add text
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes