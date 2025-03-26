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