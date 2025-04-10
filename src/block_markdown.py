def markdown_to_blocks(markdown):
    result = markdown.strip().split("\n\n")
    blocks = [block.strip() for block in result if block.strip() != ""]

    return blocks
    
