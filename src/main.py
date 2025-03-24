from textnode import TextNode,TextType

def main():
    node = TextNode("testing 123", TextType.LINK, "https://www.boot.dev")
    return node


print(main())