# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os

from openerp.tests import common
from openerp.tools.convert import convert_file


class TestConvertFile(common.TransactionCase):
    """Test convert_file method patched
    """

    def setUp(self):
        super(TestConvertFile, self).setUp()
        self.module = os.path.basename(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.imd = self.env['ir.model.data']
        self.imm = self.env['ir.module.module']
        self.fdemo = 'demo/partner_category_demo.xml'
        self.fdata = 'data/partner_category_data.xml'
        self.fdata2 = 'data/partner_category_data2.xml'
        self.funachiev = 'data/partner_category_unreachable_data.xml'
        self.funachiev2 = 'data/partner_category_unreachable_data2.xml'

    def tearDown(self):
        super(TestConvertFile, self).tearDown()
        self.imd.clear_caches()
        self.imm.clear_caches()

    def test_10_demo_ref_from_data(self):
        """Test demo referenced from data
        """
        convert_file(self.cr, self.module, self.fdemo, None, kind='demo')
        convert_file(self.cr, self.module, self.fdata, None, kind='data')

    def test_20_demo_overwritten_from_data(self):
        """Test demo overwritten from data
        """
        convert_file(self.cr, self.module, self.fdemo, None, kind='demo')
        convert_file(self.cr, self.module, self.fdata2, None, kind='data')

    def test_30_xml_id_ref_unreachable(self):
        """Test a xml_id referenced unreachable
        """
        imd_before = self.imd.search([('module', '=', self.module)])
        convert_file(self.cr, self.module, self.fdemo, None, kind='data')
        imd_after = self.imd.search([('module', '=', self.module)])
        imd_new = (imd_after - imd_before)
        imd_new.write({'module': 'unreachable'})
        convert_file(self.cr, self.module, self.funachiev, None, kind='data')

    def test_40_xml_id_overwritten_unreachable(self):
        """Test a xml_id overwritten unreachable
        """
        imd_before = self.imd.search([('module', '=', self.module)])
        convert_file(self.cr, self.module, self.fdemo, None, kind='data')
        imd_after = self.imd.search([('module', '=', self.module)])
        imd_new = (imd_after - imd_before)
        self.imm.search([('name', '=', self.module)], limit=1).copy(
            {'name': 'unreachable', 'state': 'installed'})
        imd_new.write({'module': 'unreachable'})
        convert_file(self.cr, self.module, self.funachiev2, None, kind='data')
