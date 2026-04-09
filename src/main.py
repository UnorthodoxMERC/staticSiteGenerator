from textnode import TextNode, TextType

def main():
        newNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        print(newNode)

main()