# -*- coding: utf-8 -*-
"""
    trydoc
    ------

    :copyright: Copyright 2011 by NaN Projectes de Programari Lliure, S.L.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes

from sphinx.locale import _
from sphinx.environment import NoUri
from sphinx.util.compat import Directive, make_admonition
from docutils.parsers.rst import directives
from docutils import nodes

class FieldNode(nodes.Admonition, nodes.Element): pass
#class FieldNode(nodes.Inline, nodes.TextElement): pass
class MenuNode(nodes.Admonition, nodes.Element): pass
class ViewNode(nodes.Admonition, nodes.Element): pass

#nodes._add_node_class_names('FieldNode')


class FieldDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'help': directives.flag
    }

    def run(self):
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])

        print "DIR: ", dir(self)
        print "DATA: ", self
        print "args: ", self.arguments
        print "\n\nOptions: ", self.options
        print "Content: ", self.content
        print "Line: ", self.lineno
        print "Offset: ", self.content_offset
        print "Block: ", self.block_text
        print "State: ", self.state
        print "Machine: ", self.state_machine
        print "Name: ", self.name

        field = self.arguments[0]

        if 'help' in self.options:
            show_help = True
        else:
            show_help = False

        print "T: ", type(self.block_text), type(self.content), dir(self.content)
        #content = [self.content[0]]
        content = self.content
        #block_text = self.content[0]
        block_text = self.block_text
        print "T: ", type(block_text), type(content)

        print "Field: ", field
        print "Show Help: ", show_help

        
        ad = make_admonition(FieldNode, self.name, [_('Field')], self.options,
                             content, self.lineno, self.content_offset,
                             block_text, self.state, self.state_machine)
        ad[0].line = self.lineno
        #ad = nodes.Element('hola manola')
        #ad = [nodes.TextElement('hola manola','Hola Manola')]

        #node = nodes.paragraph()
        #node.document = self.state.document
        #print "DOC: ", type(node.document), node.document

        #ad = nodes.Text('HOLA MANOLA')
        return [targetnode] + ad #+ node.children #ad

class MenuDirective(Directive):
    """
    A todo entry, displayed (if configured) in the form of an admonition.
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        # Prints only the name of the menu entry instead of its full path
        'nameonly': directives.flag, 
    }

    def run(self):
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])

        menu = self.arguments[0]

        if 'nameonly' in self.options:
            name_only = True
        else:
            name_only = False

        content = self.content
        block_text = self.block_text
        print "Menu: ", menu
        print "Name Only: ", name_only

        ad = make_admonition(MenuNode, self.name, [_('Menu')], self.options,
                             content, self.lineno, self.content_offset,
                             block_text, self.state, self.state_machine)
        ad[0].line = self.lineno
        return [targetnode] + ad
        pass

class ViewDirective(Directive):
    """
    A todo entry, displayed (if configured) in the form of an admonition.
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'field': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        targetid = 'index-%s' % env.new_serialno('index')
        targetnode = nodes.target('', '', ids=[targetid])

        view = self.arguments[0]

        field = self.options.get('field')

        content = self.content
        block_text = 'View: %s, Field: %s' % (view, field)
        print "View: ", view
        print "Field: ", field

        ad = make_admonition(ViewNode, self.name, [_('View')], self.options,
                             content, self.lineno, self.content_offset,
                             block_text, self.state, self.state_machine)
        ad[0].line = self.lineno
        return [targetnode] + ad

def process_todos(app, doctree):
    # collect all todos in the environment
    # this is not done in the directive itself because it some transformations
    # must have already been run, e.g. substitutions
    env = app.builder.env
    if not hasattr(env, 'todo_all_todos'):
        env.todo_all_todos = []
    for node in doctree.traverse(FieldNode):
        try:
            targetnode = node.parent[node.parent.index(node) - 1]
            if not isinstance(targetnode, nodes.target):
                raise IndexError
        except IndexError:
            targetnode = None
        #env.todo_all_todos.append({
        #    'docname': env.docname,
        #    'lineno': node.line,
        #    'todo': node.deepcopy(),
        #    'target': targetnode,
        #})


def visit_field_node(self, node):
    self.visit_admonition(node)

def depart_field_node(self, node):
    self.depart_admonition(node)

def visit_menu_node(self, node):
    self.visit_admonition(node)

def depart_menu_node(self, node):
    self.depart_admonition(node)

def visit_view_node(self, node):
    self.visit_admonition(node)

def depart_view_node(self, node):
    self.depart_admonition(node)

def setup(app):
    app.add_node(FieldNode,
                 html=(visit_field_node, depart_field_node),
                 latex=(visit_field_node, depart_field_node),
                 text=(visit_field_node, depart_field_node),
                 man=(visit_field_node, depart_field_node))
    app.add_node(MenuNode,
                 html=(visit_menu_node, depart_menu_node),
                 latex=(visit_menu_node, depart_menu_node),
                 text=(visit_menu_node, depart_menu_node),
                 man=(visit_menu_node, depart_menu_node))
    app.add_node(ViewNode,
                 html=(visit_view_node, depart_view_node),
                 latex=(visit_view_node, depart_view_node),
                 text=(visit_view_node, depart_view_node),
                 man=(visit_view_node, depart_view_node))

    app.add_directive('field', FieldDirective)
    app.add_directive('menu', MenuDirective)
    app.add_directive('view', ViewDirective)
    app.connect('doctree-read', process_todos)

