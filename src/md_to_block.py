def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    
    blocks = []
    
    for block in split_md:
        stripped_block = block.strip()
        if stripped_block == "":
            continue

        blocks.append(stripped_block)

    return blocks