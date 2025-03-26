import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_create_html_node(self):
        node = HTMLNode(tag="p", value="Hello", children=[], props={"href": "https://www.google.com"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"href": "https://www.google.com"})

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr_output(self):
        node = HTMLNode(tag="div", value="Hi", children=[], props={"target": "_blank"})
        expected_repr = "HTMLNode(div, Hi, 0, {'target': '_blank'})"
        self.assertEqual(repr(node), expected_repr)
        
        
if __name__ == "__main__":
    unittest.main()