# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import collections
import logging

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestShowDuplicatedItemsSelection(common.TransactionCase):

    def test_show_duplicated_items_selection(self):
        """Show a warning of all duplicated items from fields selection"""
        fields = self.env['ir.model.fields'].search([
            ('ttype', '=', 'selection'),
            ('model', '!=', 'report.account.receivable'),
        ])
        models = {}
        for field in fields:
            models.setdefault(field.model, self.env[field.model])
            sel_tuples = models[field.model]._fields[field.name].\
                _description_selection(self.env)
            sel_item_names = [str(item[0]).lower() for item in sel_tuples]
            dups = [
                dup
                for dup, count in collections.Counter(sel_item_names).items()
                if count >= 2]
            if not dups:
                continue
            module_logger = logging.getLogger(
                __name__ + '.' + field.model.replace('.', '_'))
            module_logger.warning(
                "Field selection '%s' of the model '%s' has duplicated "
                "the items '%s'.",
                field.name, field.model, ', '.join(dups),)
