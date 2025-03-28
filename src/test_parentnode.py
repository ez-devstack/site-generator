import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    def test_parent_with_multiple_leaf(self):
        child_one = LeafNode(None, "Normal text")
        child_two = LeafNode("i", "italic text")
        child_three = LeafNode(None, "Normal text")
        child_four = LeafNode("b", "Bold text")
        
        parent_node = ParentNode("p", [child_one, child_two, child_three, child_four])
        expected_html = "<p>Normal text<i>italic text</i>Normal text<b>Bold text</b></p>"
        self.assertEqual(parent_node.to_html(), expected_html)
        
    def test_parent_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])
    
if __name__ == "__main__":
    unittest.main()