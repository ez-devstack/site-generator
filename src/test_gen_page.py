import unittest
from gen_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_title_exists(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_title_with_whitespace(self):
        md = "#    Trimmed   "
        self.assertEqual(extract_title(md), "Trimmed")

    def test_title_missing(self):
        md = "## Not a title"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
