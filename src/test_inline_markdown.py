import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
    )

class TestInlineMarkdown(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic(self):
        node = TextNode("An _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("An ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code(self):
        node = TextNode("This has `code` inside", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_non_text_type(self):
        node = TextNode("Don't touch me", TextType.CODE)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [node]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [anchor](https://www.boot.dev)"
        )
        self.assertListEqual([("anchor", "https://www.boot.dev")], matches)

    def test_not_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link ![image](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
        
    def test_split_link_at_start(self):
        node = TextNode(
            "[first link](https://apple.com) is followed by text and [second link](https://burgers.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://apple.com"),
                TextNode(" is followed by text and ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://burgers.com"),
            ],
            new_nodes,
        )
        
    def test_split_link_and_image(self):
        node = TextNode(
            "I like [Boot.dev](https://www.boot.dev) and this Boots image ![cool image](https://example.com/image.png) right here.",
            TextType.TEXT,
        )

        # First apply link splitting
        link_split = split_nodes_link([node])
        # Then apply image splitting to the result of link splitting
        final_nodes = split_nodes_image(link_split)

        self.assertListEqual(
            [
                TextNode("I like ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and this Boots image ", TextType.TEXT),
                TextNode("cool image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" right here.", TextType.TEXT),
            ],
            final_nodes,
        )
        
    def test_text_to_texnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()