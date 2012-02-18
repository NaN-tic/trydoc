.. TryDoc Test documentation master file, created by
   sphinx-quickstart on Sun Nov 13 11:04:16 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TryDoc documentation
====================

Installation
------------

This extension requires the following packages:

- Sphinx 1.0 
- proteus
- tryton

Use ``pip`` to install this extension straight from the Python Package Index::

   pip install trydoc

Configuration
-------------

In order to use trydoc you should add it to the list of extensions in conf.py::

   extensions = ['sphinxcontrib.trydoc']

You should also configure proteus in conf.py with the required parameters. The 
following example will create a new sqlite database automatically::

   import proteus
   proteus.config.set_trytond(database_type='sqlite')

Usage
-----

TryDoc adds the following set of directives to be used in the docs:

Fields
~~~~~~

You can refer to any field with the following directive:

::

   .. fields:: model/field

which will print the given field name. Optionally the ``:help:`` option can be 
added. See the following example:

::

   .. fields:: ir.cron/user
      :help:

Menus
~~~~~

You can refer to any menu entry with the following directive:

::

   .. menu:: reference_to_menu_xml_id
      :nameonly:

The following code shows the full menu entry:

::

   .. menu:: ir.menu_cron_form
     
which will output *Administration / Scheduler / Scheduled Actions*. 
Appending the ``:nameonly:`` flag will only show the menu entry name: 
*Scheduled Actions*.

Views
~~~~~

You can add a screenshot of any model view with the following directive:

::

   .. view:: reference_to_view_xml_id
      :field: fieldname

where ``:field:`` is optional and will ensure the given field name is shown in 
the generated screenshot.

::

   .. view:: party.party_party_form
      :field: name

Inline usage
~~~~~~~~~~~~

Inline usage is also available either using Sphinx's mechanism:

::

   This is a reference to field |cron_user|.

   .. |cron_user| field:: ir.cron/user

or one provided by trydoc, which is shorter:

::

   This is a reference to a field @field:ir.cron/user@.

