import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_can_create(self):
        node = HTMLNode("p", "<p>Paragraph</p>", [], {})
        self.assertEqual(HTMLNode, type(node))
    
    def test_values(self):
        node = HTMLNode("p", "Paragraph", None, {"href": "https://google.com", "target":"_blank"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Paragraph")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://google.com", "target":"_blank"})

    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(props=props)
        expected = 'href="https://www.google.com" target="_blank"'
        result = node.props_to_html()
        self.assertEqual(expected, result)

    def test_repr(self):
        node = HTMLNode(tag="p")
        self.assertEqual("HTMLNode(p, None, None, None)", repr(node))


class TestLeafNode(unittest.TestCase):
    def test_can_create(self):
        node = LeafNode("p", "text", None, None)
        self.assertEqual(LeafNode, type(node))

    def test_no_value_error(self):
        node = LeafNode(tag="None")
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag_raw_text(self):
        node = LeafNode(tag=None,value="paragraph")
        expected = "paragraph"
        self.assertEqual(expected, node.to_html())

    def test_tag_html(self):
        node = LeafNode(tag="p",value="paragraph")
        expected = "<p>paragraph</p>"
        self.assertEqual(expected, node.to_html())

if __name__ == "__main__":
    unittest.main()