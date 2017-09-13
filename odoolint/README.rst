.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========
odoolint
========

Add runtime lint checks that don't are detected by odoo.

They are shown from logger.warning

- Demo xml_id referenced from data xml if the module is installed with `--without-demo=all`
- Unachievable xml_id if the module is installed with `-i module`
- Broken button If the module use a button action but is not defined on odoo
- Broken local path in `link` items of views, e.g. `<link /module_a/folder` and `/module_a/folder` is not exists.
- Duplicate items from selection fields e.g. `myfield = fields.Selection([('duplicated1', 'Duplicated1')])... myfield = fields.Selection(selection_add=[('duplicated1', 'Duplicated1')])`
- Superfluous dependency e.g. 
  - `sale_project: ['sale, 'project']`
  - `my_module: ['sale', 'base', 'sale_project', 'project']`
  `sale`, `project` and `base` are superfluous in `my_module` because `sale_project` contains them.
- Add check to validate non boolean values in boolean fields e.g.
  - `<field name="active">False</field>` It's processed like as a True and you should fix it with `<field name="customer" eval="False"/>`
  - For your information a Pull Request to change this behaviour: https://github.com/odoo/odoo/pull/13152
- Add a log error if there is a 404 code in the message of werkzeug logger
  - For your information a Pull Request to change this behaviour: https://github.com/odoo/odoo/pull/13289


Installation
============

To install this module, you need to:

#  Install with --test-enable

Usage
=====

To use this module, you need to:

#  After start the server with --test-enable review the log of this module
to check the result

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/{repo_id}/{branch}

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/{project_repo}/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Moises López <moylop260@vauxoo.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
