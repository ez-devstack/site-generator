from enum import Enum

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
