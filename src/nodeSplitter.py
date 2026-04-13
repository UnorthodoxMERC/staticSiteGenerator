from textnode import TextNode, TextType

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