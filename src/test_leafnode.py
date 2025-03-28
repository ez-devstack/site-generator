import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", None)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Testing no tag", None)
        self.assertEqual(node.to_html(), "Testing no tag")
        
    def test_leaf_props_to_html(self):
        node = LeafNode("a", "Click here", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click here</a>')
        
if __name__ == "__main__":
    unittest.main()