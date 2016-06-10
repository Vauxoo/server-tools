# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from openerp import http
from pprint import pprint

class ModuleDependenciesView(http.Controller):

    @http.route('/module/<model("ir.module.module"):module>/',
                auth='user')
    def module(self, module):
        start = datetime.now()
        depends = module.depends()
        end = datetime.now()
        computed = end - start
        return http.request.render('module_dependencies_view.module', {
            'object': module,
            'tree': depends,
            'start': start,
            'end': end,
            'computed': computed,
        })
