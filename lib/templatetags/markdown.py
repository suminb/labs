from django.template import Node, Library
from django import template
from lib.markdown2 import markdown

register = Library()

class MarkdownNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        #return markdown(context)
        return markdown(self.nodelist.render(context), extras=('footnotes', 'code-color',))

@register.tag('markdown')
def markdown_tag(parser, token):
    nodelist = parser.parse(('endmarkdown',))
    parser.delete_first_token()
    return MarkdownNode(nodelist)

#markdown = register.tag('markdown', markdown)
