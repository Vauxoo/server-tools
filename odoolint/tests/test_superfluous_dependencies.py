# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import logging

from odoo.tests import common

_logger = logging.getLogger(__name__)
MODULE = os.path.basename(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class TestSuperfluousDependencies(common.TransactionCase):
    """Test superfluous dependencies
    """

    def setUp(self):
        super(TestSuperfluousDependencies, self).setUp()
        self.imm = self.env['ir.module.module']
        self.work_module = 'document'

    def tearDown(self):
        super(TestSuperfluousDependencies, self).tearDown()
        self.imm.clear_caches()

    def create_module_superfluous_deps(self, work_module):
        """Create a module with superfluous dependencies
        Search a module with dependencies and create a new one adding
        the dependencies and sub-dependencies
        :param superfluous_work str: Name of the module of work to create it
            superfluous in dependencies of new one.
        """
        work_module = self.imm.search([('name', '=', work_module)])
        superfluous_ids = work_module.downstream_dependencies(
            exclude_states=['wo_exc'])
        self.assertTrue(superfluous_ids)
        superfluous = superfluous_ids[0]
        new_module_data = {
            'name': work_module.name + '_superfluous',
            'dependencies_id': [
                (0, 0, {'name': work_module.name}),
                (0, 0, {'name': superfluous.name}),
            ]}
        new_module = work_module.copy(new_module_data)
        return new_module

    def test_superfluous_dependencies(self):
        """Test superfluous dependencies"""
        module = self.create_module_superfluous_deps(self.work_module)
        module.compute_superfluous_dependencies()
        superfluous = module.dependencies_id.filtered('superfluous')
        self.assertEqual(superfluous.name, self.work_module)

    def get_superfluous_reason(self, work_module, superfluous):
        downstream_dependencies = self.imm.browse(
            superfluous.downstream_dependencies(exclude_states=['wo_exc']))
        reason = set(downstream_dependencies.mapped('name')) & \
            set(work_module.dependencies_id.mapped('depend_id.name'))
        return list(reason)

    def test_no_superfluous_dependencies(self):
        """Test no superfluous dependencies assuming that self.work_module
        not have"""
        work_module = self.imm.search([('name', '=', self.work_module)])
        work_module.compute_superfluous_dependencies()
        superfluous = work_module.dependencies_id.filtered('superfluous')
        self.assertFalse(
            superfluous.mapped('name'),
            superfluous.mapped('superfluous_comment'))
