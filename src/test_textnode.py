import unittest

from textnode import TextNode, TextType

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



if __name__ == "__main__":
    unittest.main()