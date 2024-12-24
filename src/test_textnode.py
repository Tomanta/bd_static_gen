import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_can_create_text_node_without_url(self):
        node = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(TextNode, type(node))
        self.assertIsNone(node.url)

    def test_can_create_text_node_with_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, url="Test")
        self.assertEqual(TextNode, type(node))
        self.assertIsNotNone(node.url)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "Javaboy")
        node2 = TextNode("This is a text node", TextType.BOLD, "Javaboy")
        self.assertEqual(node, node2)


    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "Javaboy")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


class testTextToHTML(unittest.TestCase):
    # def test_raises_error_on_invalid(self):
    #     node = TextNode("test", TextType.None)
    #     self.assertRaises(ValueError, main.text_node_to_html_node, node)

    def test_text_node(self):
        node = TextNode("test", TextType.TEXT)
        expected = LeafNode(None, "test")
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_bold_node(self):
        node = TextNode("test", TextType.BOLD)
        expected = LeafNode('b', "test")
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_italic_node(self):
        node = TextNode("test", TextType.ITALIC)
        expected = LeafNode('i', "test")
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_code_node(self):
        node = TextNode("test", TextType.CODE)
        expected = LeafNode('code', "test")
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_link_node(self):
        node = TextNode("test", TextType.LINK, url='http://fakelink.com')
        expected = LeafNode('a', "test", props={"href":"http://fakelink.com"})
        self.assertEqual(expected, text_node_to_html_node(node))

    def test_image_node(self):
        node = TextNode("img_alt_text", TextType.IMAGE,url="image.jpg")
        expected = LeafNode('img', "", props={"src":"image.jpg", "alt": "img_alt_text"})
        self.assertEqual(expected, text_node_to_html_node(node))


if __name__ == "__main__":
    unittest.main()

