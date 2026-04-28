from textnode import TextNode, TextType

from extract_md import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError('no matching closing delimiter')

        for i, node in enumerate(split_node):
            if not node:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(node, TextType.TEXT))
            else:
                new_nodes.append(TextNode(node, text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for alt, url in matches:
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for anchor, url in matches:
            sections = remaining_text.split(f"[{anchor}]({url})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining_text = sections[1]

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes        