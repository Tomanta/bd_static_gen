import unittest
from markdownblocks import markdown_to_blocks, block_to_block_type, block_to_html
from htmlnode import ParentNode, LeafNode

class TestBlockToHTML(unittest.TestCase):
    def test_block_to_html_paragraph(self):
        markdown = "This is some basic text."
        expected_html_node = ParentNode('div', children = [
            ParentNode('p', children = [
                LeafNode(value=markdown)
                ])
            ])
        self.assertEqual(expected_html_node, block_to_html(markdown))

    def test_quote_to_html(self):
        markdown = """>Quote line 1
>Quote line 2
"""
        expected_html_node = ParentNode('div', children = [
            ParentNode('blockquote', children = [
                LeafNode(None, 'Quote line 1'), LeafNode(None, 'Quote line 2')
            ])
        ])
        self.assertEqual(expected_html_node, block_to_html(markdown))

    def test_code_block(self):
        markdown = """```\nCode block line 1\nCode block line 2\n```"""
        expected_html_node = ParentNode('div', children = [ParentNode('pre', children = [
            ParentNode('code', children=[
                LeafNode(None,'Code block line 1'),
                LeafNode(None,'Code block line 2')
            ])
        ])])
        self.assertEqual(expected_html_node, block_to_html(markdown))


    def test_header_level_3(self):
        markdown = "### Header level 3"
        expected_html_node = ParentNode('div', children = [
            ParentNode('h3', children = [
                LeafNode(None, 'Header level 3')
            ])
        ])

        self.assertEqual(expected_html_node, block_to_html(markdown))


    def test_ordered_list_to_html(self):
        markdown = """1. Item 1\n2. Item 2"""
        expected_html_node = ParentNode('div', children = [
            ParentNode('ol', children = [
                ParentNode('li', children = [LeafNode(None, 'Item 1')]),
                ParentNode('li', children = [LeafNode(None, 'Item 2')])
            ])
        ])

        self.assertEqual(expected_html_node, block_to_html(markdown))


    def test_unordered_list_to_html(self):
        markdown = """* Item 1\n- Item 2"""
        expected_html_node = ParentNode('div', children = [
            ParentNode('ul', children = [
                ParentNode('li', children = [LeafNode(None, 'Item 1')]),
                ParentNode('li', children = [LeafNode(None, 'Item 2')])
            ])
        ])

        self.assertEqual(expected_html_node, block_to_html(markdown))

class TestMarkdownBlockSplit(unittest.TestCase):
    def test_basic_split(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        expected = ["# This is a heading",
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
        self.assertListEqual(expected, markdown_to_blocks(text))

class TestMarkdownBlockTypes(unittest.TestCase):
    def test_markdown_paragraph(self):
        text = "This is a normal block"
        expected = "paragraph"
        self.assertEqual(expected, block_to_block_type(text))

    def test_markdown_heading_1(self):
        text = "# This is a h1 block"
        expected = "heading"
        self.assertEqual(expected, block_to_block_type(text))

    def test_markdown_heading_2(self):
        text = "## This is a h2 block"
        expected = "heading"
        self.assertEqual(expected, block_to_block_type(text))

    def test_markdown_heading_3(self):
        text = "### This is a h3 block"
        expected = "heading"
        self.assertEqual(expected, block_to_block_type(text))

    def test_markdown_heading_4(self):
        text = "#### This is a h4 block"
        expected = "heading"
        self.assertEqual(expected, block_to_block_type(text))

    def test_markdown_heading_5(self):
        text = "##### This is a h5 block"
        expected = "heading"
        self.assertEqual(expected, block_to_block_type(text))

    def test_markdown_heading_6(self):
        text = "###### This is a h6 block"
        expected = "heading"
        self.assertEqual(expected, block_to_block_type(text))

    def test_code_block(self):
        text = "```code block\nnext line\n```"
        expected = "code"
        self.assertEqual(expected, block_to_block_type(text))

    def test_quote_block(self):
        text = ">Quote Line 1\n>Quote Line 2"
        expected = "quote"
        self.assertEqual(expected, block_to_block_type(text))

    def test_not_quote_block(self):
        text = ">Quote Line 1\nQuote Line 2"
        expected = "paragraph"
        self.assertEqual(expected, block_to_block_type(text))


    def test_unordered_list(self):
        text = "* List item 1\n* List item 2"
        expected = "unordered_list"
        self.assertEqual(expected, block_to_block_type(text))

    def test_not_unordered_list(self):
        text = "* List item 1\n*List item 2"
        expected = "paragraph"
        self.assertEqual(expected, block_to_block_type(text))

    def test_ordered_list(self):
        text = "1. List Item 1\n2. List item 2\n3. List item 3"
        expected = "ordered_list"
        self.assertEqual(expected, block_to_block_type(text))

    def test_ordered_list_sequence(self):
        text = "1. List item 1\n2. List item 2\n4. List item 4"
        expected = "paragraph"
        self.assertEqual(expected, block_to_block_type(text))



if __name__ == "__main__":
    unittest.main()