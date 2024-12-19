import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image, split_nodes_link,
    text_to_textnodes
)
from textnode import TextNode, TextType

class testInlineMarkdown(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),            
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded",TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded",TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_delim_italic(self):
        pass

    def test_delim_bold_and_italic(self):
        pass

    def test_bold_multiword(self):
        pass

    def test_invalid_markdown(self):
        node = TextNode("This is *invalid", TextType.TEXT)
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "*", TextType.BOLD)


class testMarkdownImages(unittest.TestCase):
    def test_extract_basic_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        results = extract_markdown_images(text)
        expected =  [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(expected, results)

    def test_image_extract_ignores_urls(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        results = extract_markdown_images(text)
        self.assertListEqual([],results)

    def test_split_image_nodes(self):
        node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, split_nodes_image([node]))

    def test_split_image_and_link(self):
        node = TextNode("This is a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a [link](https://www.boot.dev)", TextType.TEXT)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and a [link](https://www.boot.dev)", TextType.TEXT)
        ]
        self.assertListEqual(expected, split_nodes_image([node]))        

class testMarkdownLinks(unittest.TestCase):
    def test_extract_basic_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        results = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(expected, results)

    def test_link_extract_ignores_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        results = extract_markdown_links(text)
        self.assertListEqual([],results)

    def test_split_link_nodes(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, split_nodes_link([node]))

    def test_split_link_and_image(self):
        node = TextNode("This is a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a [link](https://www.boot.dev)", TextType.TEXT)
        expected = [
            TextNode("This is a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="https://www.boot.dev"),
        ]
        self.assertListEqual(expected, split_nodes_link([node]))

class testTextToTextNodes(unittest.TestCase):
    def test_bold_link_parsing(self):
        text = "This is **text** with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_bold_image_parsing(self):
        text = "This is **text** with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_image_and_link_parsing(self):
        text = "This is a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a [link](https://www.boot.dev) and more text"
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and more text", TextType.TEXT),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_basic_text_parsing(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="https://boot.dev"),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))

if __name__ == "__main__":
    unittest.main()
