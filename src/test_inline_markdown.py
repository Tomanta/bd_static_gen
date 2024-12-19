import unittest
from inline_markdown import split_nodes_delimiter
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

if __name__ == "__main__":
    unittest.main()
