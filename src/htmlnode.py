from typing import Optional, List, Dict

class HTMLNode():
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List['HTMLNode']] = None,
        props: Optional[Dict[str, str]] = None
        ):
        
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}
        
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None: return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {len(self.children)}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props
        
    def to_html(self):
        if self.tag is None:
            return self.value
        
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not children:
            raise ValueError("Child of ParentNode required")
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode tag required")
        
        parent_html = ''.join(child.to_html() for child in self.children)
        return f"<{self.tag}>{parent_html}</{self.tag}>"