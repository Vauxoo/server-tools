# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from StringIO import StringIO

from lxml import etree

from openerp.modules import get_module_resource
from openerp.tests import common


@common.at_install(False)
@common.post_install(True)
class TestShowBrokenLink(common.TransactionCase):
    def test_show_broken_link(self):
        """Show a warning of all broken link cases"""
        views = self.env['ir.ui.view'].search([('arch', 'ilike', '%<link %')])
        for view in views:
            doc = etree.parse(StringIO(view.arch))
            for link in doc.xpath("//link"):
                href = link.attrib.get('href')
                if href and href.startswith('/'):
                    module = href.split('/')[1]
                    url = href.replace('/' + module + '/', '')
                    path = get_module_resource(module, url)
                    if path:
                        continue
                    xml_ids = view._get_xml_ids()
                    xmlid = xml_ids and xml_ids.values()[0][0] or ''
                    current_module, xml_id = xmlid.split('.')
                    module_logger = logging.getLogger(
                        __name__ + '.' + current_module)
                    module_logger.warning("View '%s' has broken url '%s'.",
                                          xml_id, href)
