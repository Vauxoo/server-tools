# -*- coding: utf-8 -*-

import json
from openerp import models, api

class module_dependencies_view(models.Model):
    _inherit = 'ir.module.module'
    _fields_read = ['name', 'icon', 'display_name', 'installed_version']

    @api.model
    def get_depends(self, module):
        return module.dependencies_id.mapped('depend_id')

    @api.model
    def get_depends_dict(self, module):
        module_dict = module.read(module._fields_read)[0]
        module_dict.pop('id')
        deps = module.get_depends(module)
        children = []
        for d in deps:
            grand_children = self.get_depends_dict(d)
            children.append(grand_children)
        module_dict.update({'children': children})
        return module_dict

    @api.model
    def depends(self):
        module = self.get_depends_dict(self)
        return json.dumps(module)

    @api.multi
    def open_diagram(self):
        self.ensure_one()
        diagram_url = "/module/%i" % self.id
        action = {
            'type': 'ir.actions.act_url',
            'name': "Diagram View.",
            'target': "new",
            'context': self._context,
            'url': diagram_url,
        }
        return action
