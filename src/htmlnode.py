class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        string = ''
        if self.props == None:
            return string
        for key in self.props:
            string += f' {key}="{self.props[key]}"'
        return string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError('leaf nodes must have a value')
        
        if self.tag is None:
            return f'{self.value}'
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('parent nodes must have a tag')
        
        if self.children is None:
            raise ValueError('parent nodes must have children')
        
        HTMLString = f'<{self.tag}{self.props_to_html()}>'
        
        for child in self.children:
            HTMLString += child.to_html()

        HTMLString += f'</{self.tag}>'

        return HTMLString