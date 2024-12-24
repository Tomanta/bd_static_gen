import unittest
from convert_md_to_html import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_invalid_markdown_raises_error(self):
        invalid_markdown = "### Test Header"
        self.assertRaises(ValueError, extract_title, invalid_markdown)

    def test_extracts_header(self):
        valid_markdown = "# Header Text\n\nStandard text block."
        expected = "Header Text"
        self.assertEqual(expected, extract_title(valid_markdown))