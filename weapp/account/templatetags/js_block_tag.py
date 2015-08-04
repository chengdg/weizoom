#from collections import defaultdict

from django.conf import settings
from django.template.base import TemplateSyntaxError, Library, Node, TextNode,\
    token_kwargs, Variable
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.utils import six

register = Library()

BLOCK_CONTEXT_KEY = 'block_context'

class ExtendsError(Exception):
    pass

class JsBlockNode(Node):
    def __init__(self, name, nodelist, parent=None):
        self.name, self.nodelist, self.parent = name, nodelist, parent

    def __repr__(self):
        return "<JsBlock Node: %s. Contents: %r>" % (self.name, self.nodelist)

    def render(self, context):
        block_context = context.render_context.get(BLOCK_CONTEXT_KEY)
        context.push()
        if block_context is None:
            context['jsblock'] = self
            result = self.nodelist.render(context)
        else:
            push = block = block_context.pop(self.name)
            if block is None:
                block = self
            # Create new block so we can store context without thread-safety issues.
            block = JsBlockNode(block.name, block.nodelist)
            block.context = context
            context['jsblock'] = block
            result = block.nodelist.render(context)
            if push is not None:
                block_context.push(self.name, push)
        context.pop()

        beg = result.find('>')
        end = result.rfind('<')
        result = result[beg+1:end]
        return result

    def super(self):
        render_context = self.context.render_context
        if (BLOCK_CONTEXT_KEY in render_context and
            render_context[BLOCK_CONTEXT_KEY].get_block(self.name) is not None):
            return mark_safe(self.render(self.context))
        return ''


@register.tag('jsblock')
def do_js_block(parser, token):
    """
    Define a js block that can be overridden by child templates. and remove <script> tag.
    """
    # token.split_contents() isn't useful here because this tag doesn't accept variable as arguments
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' tag takes only one argument" % bits[0])
    block_name = bits[1]
    # Keep track of the names of BlockNodes found in this template, so we can
    # check for duplication.
    try:
        if block_name in parser.__loaded_blocks:
            raise TemplateSyntaxError("'%s' tag with name '%s' appears more than once" % (bits[0], block_name))
        parser.__loaded_blocks.append(block_name)
    except AttributeError: # parser.__loaded_blocks isn't a list yet
        parser.__loaded_blocks = [block_name]
    nodelist = parser.parse(('endjsblock',))

    # This check is kept for backwards-compatibility. See #3100.
    endblock = parser.next_token()
    acceptable_endblocks = ('endjsblock', 'endjsblock %s' % block_name)
    if endblock.contents not in acceptable_endblocks:
        parser.invalid_block_tag(endblock, 'endjsblock', acceptable_endblocks)

    return JsBlockNode(block_name, nodelist)
