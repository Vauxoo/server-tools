# -*- coding: utf-8 -*-
from datetime import datetime
from openerp import http


class ModuleDependenciesView(http.Controller):

    @http.route('/module/one/<model("ir.module.module"):module>/',
                auth='user')
    def module_level(self, module):
        start = datetime.now()
        depends = module.with_context({'one_level': True}).depends()
        end = datetime.now()
        computed = end - start
        return http.request.render('module_dependencies_view.module', {
            'object': module,
            'tree': depends,
            'start': start,
            'end': end,
            'computed': computed,
        })

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

    @http.route('/module/dendrogram/<model("ir.module.module"):module>/',
                auth='user')
    def cluster_dendgram(self, module):
        depends = module.with_context({'with_id': True}).depends()
        return depends

    @http.route('/module/mesh/<model("ir.module.module"):module>/',
                auth='user')
    def module_mesh(self, module):
        start = datetime.now()
        depends = module.depends()
        end = datetime.now()
        computed = end - start
        return http.request.render(
            'module_dependencies_view.cluster_dendrogram', {
                'object': module,
                'tree': depends,
                'start': start,
                'end': end,
                'computed': computed,
            })
