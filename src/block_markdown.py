from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_blocks(markdown):
    result = markdown.strip().split("\n\n")
    blocks = [block.strip() for block in result if block.strip() != ""]

    return blocks
    
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"
    
def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.ULIST
    
    lines = block.splitlines()
    for i, line in enumerate(lines, start=1):
        expected_start = f"{i}. "
        if not line.startswith(expected_start):
            break
    else:
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH

def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def heading_block_to_html(block):
    level = block.count('#', 0, block.find(' '))
    tag = f"h{level}"
    content = block[level+1:].strip()
    return ParentNode(tag, text_to_children(content))

def paragraph_block_to_html(block):
    normalized_text = block.replace("\n", " ")
    return ParentNode("p", text_to_children(normalized_text))

def quote_block_to_html(block):
    stripped = "\n".join(line[1:].strip() for line in block.splitlines())
    return ParentNode("blockquote", text_to_children(stripped))

def code_block_to_html(block):
    content = "\n".join(block.splitlines()[1:-1])
    text_node = text_node_to_html_node(TextNode(content + "\n", TextType.CODE))
    return ParentNode("pre", [text_node])

def unordered_list_block_to_html(block):
    items = block.splitlines()
    li_nodes = [ParentNode("li", text_to_children(item[2:].strip())) for item in items]
    return ParentNode("ul", li_nodes)

def ordered_list_block_to_html(block):
    items = block.splitlines()
    li_nodes = [ParentNode("li", text_to_children(item[item.find('.')+2:].strip())) for item in items]
    return ParentNode("ol", li_nodes)

def convert_block_to_html(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return heading_block_to_html(block)
    elif block_type == BlockType.PARAGRAPH:
        return paragraph_block_to_html(block)
    elif block_type == BlockType.QUOTE:
        return quote_block_to_html(block)
    elif block_type == BlockType.CODE:
        return code_block_to_html(block)
    elif block_type == BlockType.ULIST:
        return unordered_list_block_to_html(block)
    elif block_type == BlockType.OLIST:
        return ordered_list_block_to_html(block)
    else:
        raise Exception(f"Unhandled block type: {block_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [convert_block_to_html(block) for block in blocks]
    return ParentNode("div", children)