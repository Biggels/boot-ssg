from textnode import TextNode, TextType


def main():
    test_node = TextNode("this is some bolded text", TextType.BOLD)
    print(test_node)


if __name__ == "__main__":
    main()
