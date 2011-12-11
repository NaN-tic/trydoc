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
from docutils.parsers.rst import directives, states
from docutils import nodes

from docutils.parsers.rst.directives.images import Image
from docutils.parsers.rst.directives.misc import Replace

from proteus import config, Model

class FieldDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
            'help': directives.flag
            }

    def run(self):
        content = self.arguments[0]
        if 'help' in self.options:
            show_help = True
        else:
            show_help = False

        model_name, field_name = content.split('/')

        ModelClass = Model.get('ir.model')
        models = ModelClass.find([
                ('model', '=', model_name),
                ])
        if not models:
            return [self.state_machine.reporter.warning(
                    'Model "%s" not found.' % model_name, line=self.lineno)]

        ModelField = Model.get('ir.model.field')
        field = ModelField.find([
                ('name', '=', field_name),
                ('model', '=', models[0].id),
                ])[0]

        text = ''
        for field in models[0].fields:
            if field.name == field_name:
                if show_help:
                    if field.help:
                        text = field.help
                    else:
                        text = 'Field "%s" has no help available' % content
                else:
                    if field.field_description:
                        text = field.field_description
                    else:
                        text = 'Field "%s" has no description available' % content
                break

        text = '*%s*' % text
        return [nodes.Text(text)]
        
class MenuDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
            # Prints only the name of the menu entry instead of its full path
            'nameonly': directives.flag, 
            }

    def run(self):
        content = self.arguments[0]
        if 'nameonly' in self.options:
            show_name_only = True
        else:
            show_name_only = False

        module_name, fs_id = content.split('.')

        ModelData = Model.get('ir.model.data')
        #db_id = ModelData.get_id(module_name, fs_id)

        records = ModelData.find([
                ('module', '=', module_name),
                ('fs_id', '=', fs_id),
                ('model', '=', 'ir.ui.menu'),
                ])
        if not records:
            return [self.state_machine.reporter.warning(
                    'Menu entry "%s" not found.' % content, line=self.lineno)]
        db_id = records[0].db_id

        Menu = Model.get('ir.ui.menu')
        menu = Menu(db_id)
        if show_name_only:
            text = menu.name
        else:
            text = menu.complete_name

        text = '*%s*' % text

        return [nodes.Text(text)]


class ViewDirective(Image):
    option_spec = Image.option_spec.copy()
    option_spec.update({
            'field': directives.unchanged,
            })

    def run(self):
        view = str(self.arguments[0])
        field = self.options.get('field')

        # TODO: Create snapshot

        self.arguments[0] = 'tryton-test.png'
        image_node_list = Image.run(self)
        return image_node_list


def init_proteus(app):
    config.set_trytond(database_type='sqlite')

def setup(app):
    app.add_config_value('trydoc_server', None, 'env')

    app.add_directive('field', FieldDirective)
    app.add_directive('menu', MenuDirective)
    app.add_directive('view', ViewDirective)

    app.connect('builder-inited', init_proteus)
