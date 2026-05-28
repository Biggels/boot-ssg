class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(
            "Child classes should override this method to render themselves as HTML."
        )

    def props_to_html(self):
        attr_str = ""
        if not self.props:
            return attr_str

        for attr, value in self.props.items():
            attr_str += f' {attr}="{value}"'
        return attr_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
