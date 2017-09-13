# -*- coding: utf-8 -*-
{
    'name': "module_dependencies_view",
    'version': '10.0.0.0.0',
    'author': 'Vauxoo, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'website': 'https://www.vauxoo.com',
    'category': 'Uncategorized',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'views/templates.xml',
        'views/view.xml',
    ],
    'installable': True,
}
