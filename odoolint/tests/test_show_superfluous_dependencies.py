# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestShowSuperfluousDependencies(common.TransactionCase):
    def test_show_superfluous_dependencies(self):
        """Show a warning of all the superfluous dependency cases"""
        modules = self.env['ir.module.module'].search([
            ('state', '=', 'installed')])
        modules.compute_superfluous_dependencies()
        dependencies = \
            modules.mapped('dependencies_id').filtered('superfluous')
        for dependency in dependencies:
            module_logger = logging.getLogger(
                __name__ + '.' + dependency.module_id.name)
            module_logger.info(dependency.superfluous_comment)
