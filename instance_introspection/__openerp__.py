# coding: utf-8
# © 2015 Vauxoo - http://www.vauxoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# info Vauxoo (info@vauxoo.com)
# coded by: nhomar@vauxoo.com
# planned by: nhomar@vauxoo.com

{
    "name": "Instance Instrospection",
    "version": "9.0.0.0.0",
    "author": "Vauxoo, Odoo Community Association (OCA)",
    "category": "Tecnhical Features",
    "website": "http://www.vauxoo.com/",
    "license": "AGPL-3",
    "depends": ["web"],
    "demo": [],
    "images": [
        "static/src/img/image.png",
    ],
    "data": [
        'views/instance_introspection_view.xml',
        'views/instance_view.xml',
    ],
    "external_dependencies": {
        "python": [
            "pip"
        ],
    },
    "installable": True,
}
