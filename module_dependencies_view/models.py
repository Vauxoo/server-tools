# -*- coding: utf-8 -*-

import json
from openerp import models, api


class module_dependencies_view(models.Model):
    _inherit = 'ir.module.module'
    _fields_read = [
        'name',
        'icon',
        'display_name',
        'installed_version',
        'author',
        'installed_version',
    ]

    @api.model
    def get_depends(self, module):
        return module.dependencies_id.mapped('depend_id')

    # Tis method is extracted from odoo/odoo v9.0
    @api.multi
    # pylint: disable=dangerous-default-value
    def _get_dependencies_ids(
            self, mod_ids, known_dep_ids=None,
            exclude_states=['installed', 'uninstallable', 'to remove']):
        """Copied from odoo native ir.module.module v9.0
        Return the dependency tree of modules of the given `ids`, and that
        satisfy the `exclude_states` filter """
        # It to avoid overwrite the original method
        ids = mod_ids
        cr = self.env.cr
        if not ids:
            return []
        known_dep_ids = set(known_dep_ids or [])
        cr.execute(
            '''SELECT DISTINCT m.id
            FROM
                ir_module_module_dependency d
            JOIN
                ir_module_module m ON (d.module_id=m.id)
            WHERE
                m.name IN (
                    SELECT name
                    from ir_module_module_dependency
                    where module_id in %s) AND
                m.state NOT IN %s AND
                m.id NOT IN %s ''',
            (tuple(ids), tuple(exclude_states), tuple(known_dep_ids or ids)))
        new_dep_ids = set([m[0] for m in cr.fetchall()])
        missing_mod_ids = new_dep_ids - known_dep_ids
        known_dep_ids |= new_dep_ids
        if missing_mod_ids:
            known_dep_ids |= set(
                self._get_dependencies_ids(
                    list(missing_mod_ids), known_dep_ids, exclude_states))
        return list(known_dep_ids)

    @api.model
    def get_depends_dict_one(self, module):
        '''Return dependencies as dict but only one level with all necesary
        dependencies for a module.'''
        module_dict = module.read(module._fields_read)[0]
        dependency_ids = module._get_dependencies_ids(
            [module.id], exclude_states=['to_remove'])
        module_dict = self.set_color(module_dict)
        full_deps = self.search_read([('id', 'in', dependency_ids)],
                                     self._fields_read)
        full_deps = [self.set_color(fd) for fd in full_deps]
        module_dict.update({'children': full_deps})
        return module_dict

    @api.model
    def get_depends_dict(self, module):
        context = dict(self._context)

        module_dict = module.read(module._fields_read)[0]
        module_dict = self.set_color(module_dict)
        if not context.get('with_id'):
            module_dict.pop('id')
        deps = module.get_depends(module)
        children = []

        for d in deps:
            grand_children = self.get_depends_dict(d)
            children.append(grand_children)

        module_dict.update({'children': children})

        return module_dict

    @api.multi
    def depends(self):
        context = dict(self._context)
        if context.get('one_level'):
            module = self.get_depends_dict_one(self)
        if not context.get('one_level'):
            module = self.get_depends_dict(self)
        return json.dumps(module)

    @api.multi
    def open_diagram_one_level(self):
        self.ensure_one()
        diagram_url = "/module/one/%i" % self.id
        action = {
            'type': 'ir.actions.act_url',
            'name': "Diagram View.",
            'target': "new",
            'context': self._context,
            'url': diagram_url,
        }
        return action

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

    # Back list is the list of modules not listed into runbot.odoo.com
    # Then dependency must be reviewed.
    _odoo_black_list = [
        'auth_ldap',
        'base_gengo',
        'hw_blackbox_be',
        'hw_escpos',
        'hw_posbox_homepage',
        'hw_posbox_upgrade',
        'hw_proxy',
        'hw_scale',
        'hw_scanner',
        'l10n_ae',
        'l10n_ar',
        'l10n_at',
        'l10n_be',
        'l10n_be_coda',
        'l10n_be_hr_payroll',
        'l10n_be_hr_payroll_account',
        'l10n_be_intrastat',
        'l10n_be_invoice_bba',
        'l10n_bo',
        'l10n_br',
        'l10n_ca',
        'l10n_ch',
        'l10n_cl',
        'l10n_cn',
        'l10n_co',
        'l10n_cr',
        'l10n_de',
        'l10n_do',
        'l10n_ec',
        'l10n_es',
        'l10n_et',
        'l10n_eu_service',
        'l10n_fr',
        'l10n_fr_hr_payroll',
        'l10n_fr_rib',
        'l10n_gr',
        'l10n_gt',
        'l10n_hn',
        'l10n_hr',
        'l10n_hu',
        'l10n_in',
        'l10n_in_hr_payroll',
        'l10n_it',
        'l10n_jp',
        'l10n_lu',
        'l10n_ma',
        'l10n_multilang',
        'l10n_mx',
        'l10n_nl',
        'l10n_no',
        'l10n_pa',
        'l10n_pe',
        'l10n_pl',
        'l10n_pt',
        'l10n_ro',
        'l10n_sa',
        'l10n_sg',
        'l10n_si',
        'l10n_syscohada',
        'l10n_th',
        'l10n_tr',
        'l10n_uk',
        'l10n_us',
        'l10n_uy',
        'l10n_ve',
        'l10n_vn',
        'website_gengo',
        'website_instantclick',
        ]
    _odoo_modules = [
        'account',
        'account_accountant',
        'account_analytic_analysis',
        'account_analytic_default',
        'account_analytic_plans',
        'account_anglo_saxon',
        'account_asset',
        'account_bank_statement_extensions',
        'account_budget',
        'account_cancel',
        'account_chart',
        'account_check_writing',
        'account_followup',
        'account_payment',
        'account_sequence',
        'account_test',
        'account_voucher',
        'analytic',
        'analytic_contract_hr_expense',
        'analytic_user_function',
        'anonymization',
        'association',
        'auth_crypt',
        'auth_ldap',
        'auth_oauth',
        'auth_openid',
        'auth_signup',
        'base',
        'base_action_rule',
        'base_gengo',
        'base_geolocalize',
        'base_iban',
        'base_import',
        'base_import_module',
        'base_report_designer',
        'base_setup',
        'base_vat',
        'board',
        'bus',
        'calendar',
        'claim_from_delivery',
        'contacts',
        'crm',
        'crm_claim',
        'crm_helpdesk',
        'crm_mass_mailing',
        'crm_partner_assign',
        'crm_profiling',
        'crm_project_issue',
        'decimal_precision',
        'delivery',
        'document',
        'edi',
        'email_template',
        'event',
        'event_sale',
        'fetchmail',
        'fleet',
        'gamification',
        'gamification_sale_crm',
        'google_account',
        'google_calendar',
        'google_drive',
        'google_spreadsheet',
        'hr',
        'hr_applicant_document',
        'hr_attendance',
        'hr_contract',
        'hr_evaluation',
        'hr_expense',
        'hr_gamification',
        'hr_holidays',
        'hr_payroll',
        'hr_payroll_account',
        'hr_recruitment',
        'hr_timesheet',
        'hr_timesheet_invoice',
        'hr_timesheet_sheet',
        'hw_blackbox_be',
        'hw_escpos',
        'hw_posbox_homepage',
        'hw_posbox_upgrade',
        'hw_proxy',
        'hw_scale',
        'hw_scanner',
        'im_chat',
        'im_livechat',
        'im_odoo_support',
        'knowledge',
        'l10n_ae',
        'l10n_ar',
        'l10n_at',
        'l10n_be',
        'l10n_be_coda',
        'l10n_be_hr_payroll',
        'l10n_be_hr_payroll_account',
        'l10n_be_intrastat',
        'l10n_be_invoice_bba',
        'l10n_bo',
        'l10n_br',
        'l10n_ca',
        'l10n_ch',
        'l10n_cl',
        'l10n_cn',
        'l10n_co',
        'l10n_cr',
        'l10n_de',
        'l10n_do',
        'l10n_ec',
        'l10n_es',
        'l10n_et',
        'l10n_eu_service',
        'l10n_fr',
        'l10n_fr_hr_payroll',
        'l10n_fr_rib',
        'l10n_gr',
        'l10n_gt',
        'l10n_hn',
        'l10n_hr',
        'l10n_hu',
        'l10n_in',
        'l10n_in_hr_payroll',
        'l10n_it',
        'l10n_jp',
        'l10n_lu',
        'l10n_ma',
        'l10n_multilang',
        'l10n_mx',
        'l10n_nl',
        'l10n_no',
        'l10n_pa',
        'l10n_pe',
        'l10n_pl',
        'l10n_pt',
        'l10n_ro',
        'l10n_sa',
        'l10n_sg',
        'l10n_si',
        'l10n_syscohada',
        'l10n_th',
        'l10n_tr',
        'l10n_uk',
        'l10n_us',
        'l10n_uy',
        'l10n_ve',
        'l10n_vn',
        'lunch',
        'mail',
        'marketing',
        'marketing_campaign',
        'marketing_campaign_crm_demo',
        'marketing_crm',
        'mass_mailing',
        'membership',
        'mrp',
        'mrp_byproduct',
        'mrp_operations',
        'mrp_repair',
        'multi_company',
        'note',
        'note_pad',
        'pad',
        'pad_project',
        'payment',
        'payment_adyen',
        'payment_authorize',
        'payment_buckaroo',
        'payment_ogone',
        'payment_paypal',
        'payment_sips',
        'payment_transfer',
        'point_of_sale',
        'portal',
        'portal_claim',
        'portal_gamification',
        'portal_project',
        'portal_project_issue',
        'portal_sale',
        'portal_stock',
        'pos_discount',
        'pos_restaurant',
        'procurement',
        'procurement_jit',
        'procurement_jit_stock',
        'product',
        'product_email_template',
        'product_expiry',
        'product_extended',
        'product_margin',
        'product_visible_discount',
        'project',
        'project_issue',
        'project_issue_sheet',
        'project_timesheet',
        'purchase',
        'purchase_analytic_plans',
        'purchase_double_validation',
        'purchase_requisition',
        'report',
        'report_intrastat',
        'report_webkit',
        'resource',
        'sale',
        'sale_analytic_plans',
        'sale_crm',
        'sale_journal',
        'sale_layout',
        'sale_margin',
        'sale_mrp',
        'sale_order_dates',
        'sale_service',
        'sale_stock',
        'sales_team',
        'share',
        'stock',
        'stock_account',
        'stock_dropshipping',
        'stock_invoice_directly',
        'stock_landed_costs',
        'stock_picking_wave',
        'subscription',
        'survey',
        'survey_crm',
        'test_access_rights',
        'test_convert',
        'test_converter',
        'test_documentation_examples',
        'test_exceptions',
        'test_impex',
        'test_inherit',
        'test_inherits',
        'test_limits',
        'test_new_api',
        'test_uninstall',
        'test_workflow',
        'warning',
        'web',
        'web_analytics',
        'web_api',
        'web_calendar',
        'web_diagram',
        'web_gantt',
        'web_graph',
        'web_kanban',
        'web_kanban_gauge',
        'web_kanban_sparkline',
        'web_linkedin',
        'web_tests',
        'web_tests_demo',
        'web_view_editor',
        'website',
        'website_blog',
        'website_certification',
        'website_crm',
        'website_crm_partner_assign',
        'website_customer',
        'website_event',
        'website_event_sale',
        'website_event_track',
        'website_forum',
        'website_forum_doc',
        'website_gengo',
        'website_google_map',
        'website_hr',
        'website_hr_recruitment',
        'website_instantclick',
        'website_livechat',
        'website_less',  # From themes
        'website_mail',
        'website_mail_group',
        'website_membership',
        'website_partner',
        'website_payment',
        'website_project',
        'website_quote',
        'website_report',
        'website_sale',
        'website_sale_delivery',
        'website_sale_options',
        'website_twitter',
    ]

    @api.multi
    def set_color(self, module_dict):
        module_dict['color'] = 'lightsteelblue'
        module_dict['color_open'] = 'lightyellow'
        if module_dict.get('name') in self._odoo_modules:
            module_dict['color'] = 'yellowgreen'
            module_dict['color_open'] = 'mediumaquamarine'
        return module_dict
