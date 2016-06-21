# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from StringIO import StringIO

from lxml import etree

from openerp.tests import common


@common.at_install(False)
@common.post_install(True)
class TestShowBrokenButton(common.TransactionCase):
    def test_show_broken_button(self):
        """Show a warning of all broken button cases"""
        # TODO: Consider QWEB with button
        views = self.env['ir.ui.view'].search([('arch', 'ilike', '%<button %'),
                                               ('type', '!=', 'qweb')])
        for view in views:
            doc = etree.parse(StringIO(view.arch))
            for button in doc.xpath("//button"):
                button_type = button.attrib.get('type')
                # button type 'action' use ref(xml_id) then
                # we don't need consider it because
                # the check of xml unreachable will detect them
                if button_type == 'object':
                    model_name = view.model
                    method_name = button.attrib.get('name')
                    try:
                        model = self.env[model_name]
                    except KeyError:
                        continue
                    if not method_name:
                        continue
                    has_button_method = hasattr(model, method_name)
                    if has_button_method:
                        continue
                    invalid_parent = None
                    for ancestor in button.iterancestors():
                        if ancestor.tag == 'field':
                            invalid_parent = ancestor
                            break
                        elif ancestor.tag == 'xpath':
                            invalid_parent = ancestor
                            break
                    if invalid_parent is not None:
                        # TODO: Consider sub-views of *2many fields.
                        # TODO: Consider inherit from xpath for *2many fields.
                        continue
                    xml_ids = view._get_xml_ids()
                    xmlid = xml_ids and xml_ids.values()[0][0] or '.'
                    current_module, xml_id = xmlid.split('.')
                    module_logger = logging.getLogger(
                        __name__ + '.' + current_module)
                    module_logger.warning("View '%s' has broken button '%s'",
                                          xml_id, method_name)

                elif not button_type:
                    # TODO: Add a warning to specify button type
                    # module_logger.warning(
                    #     "View '%s' has a button '%s' without type",
                    #     xml_id, method_name)
                    pass
