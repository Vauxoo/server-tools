# -*- coding: utf-8 -*-

import json
from openerp import models, api


class ModuleDependenciesView(models.Model):
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

    @api.multi
    def _get_dependencies_ids(
            self, known_deps=None,
            exclude_states=('uninstalled', 'uninstallable', 'to remove')):
        """Copied from odoo native ir.module.module v10.0
        Return the dependency tree of modules of the given `ids`, and that
        satisfy the `exclude_states` filter """
        # It to avoid overwrite the original method
        if not self:
            return self
        known_deps = known_deps or self.browse()
        query = """ SELECT DISTINCT m.id
                    FROM ir_module_module_dependency d
                    JOIN ir_module_module m ON (d.module_id=m.id)
                    WHERE
                        m.name IN (
                            SELECT name
                            from ir_module_module_dependency
                            where module_id in %s) AND
                        m.state NOT IN %s AND
                        m.id NOT IN %s """
        self._cr.execute(query, (tuple(self.ids), tuple(exclude_states),
                                 tuple(known_deps.ids or self.ids)))
        new_deps = self.browse([row[0] for row in self._cr.fetchall()])
        missing_mods = new_deps - known_deps
        known_deps |= new_deps
        if missing_mods:
            known_deps |= missing_mods._get_dependencies_ids(
                known_deps, exclude_states)
        return known_deps

    @api.model
    def get_depends_dict_one(self, module):
        """Return dependencies as dict but only one level with all necesary
        dependencies for a module."""
        module_dict = module.read(module._fields_read)[0]
        dependency_ids = module._get_dependencies_ids(
            exclude_states=['to_remove'])
        module_dict = self.set_color(module_dict)
        full_deps = self.search_read(
            [('id', 'in', dependency_ids.mapped('id'))], self._fields_read)
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
        for dep in deps:
            grand_children = self.get_depends_dict(dep)
            children.append(grand_children)
        module_dict.update({'children': children})
        return module_dict

    @api.multi
    def depends(self):
        self.ensure_one()
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

    _odoo_modules = [
        'account',
        'account_accountant',
        'account_analytic_default',
        'account_asset',
        'account_bank_statement_import',
        'account_budget',
        'account_cancel',
        'account_check_printing',
        'account_tax_cash_basis',
        'account_tax_python',
        'account_test',
        'account_voucher',
        'analytic',
        'anonymization',
        'association',
        'auth_crypt',
        'auth_ldap',
        'auth_oauth',
        'auth_signup',
        'barcodes',
        'base_action_rule',
        'base_address_city',
        'base_address_extended',
        'base_gengo',
        'base_geolocalize',
        'base_iban',
        'base_import',
        'base_import_module',
        'base_setup',
        'base_vat',
        'board',
        'bus',
        'calendar',
        'contacts',
        'crm',
        'crm_project_issue',
        'decimal_precision',
        'delivery',
        'document',
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
        'hr_attendance',
        'hr_contract',
        'hr_expense',
        'hr_expense_check',
        'hr_gamification',
        'hr_holidays',
        'hr_maintenance',
        'hr_payroll',
        'hr_payroll_account',
        'hr_recruitment',
        'hr_recruitment_survey',
        'hr_timesheet',
        'hr_timesheet_attendance',
        'hr_timesheet_sheet',
        'hw_blackbox_be',
        'hw_escpos',
        'hw_posbox_homepage',
        'hw_posbox_upgrade',
        'hw_proxy',
        'hw_scale',
        'hw_scanner',
        'hw_screen',
        'im_livechat',
        'l10n_ae',
        'l10n_ar',
        'l10n_at',
        'l10n_au',
        'l10n_be',
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
        'l10n_cn_small_business',
        'l10n_cn_standard',
        'l10n_co',
        'l10n_cr',
        'l10n_de',
        'l10n_de_skr03',
        'l10n_de_skr04',
        'l10n_do',
        'l10n_ec',
        'l10n_es',
        'l10n_et',
        'l10n_eu_service',
        'l10n_fr',
        'l10n_fr_certification',
        'l10n_fr_fec',
        'l10n_fr_hr_payroll',
        'l10n_generic_coa',
        'l10n_gr',
        'l10n_gt',
        'l10n_hn',
        'l10n_hr',
        'l10n_hu',
        'l10n_in',
        'l10n_in_hr_payroll',
        'l10n_in_schedule6',
        'l10n_it',
        'l10n_jp',
        'l10n_lu',
        'l10n_ma',
        'l10n_multilang',
        'l10n_mx',
        'l10n_nl',
        'l10n_no',
        'l10n_nz',
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
        'link_tracker',
        'lunch',
        'mail',
        'maintenance',
        'marketing_campaign',
        'marketing_campaign_crm_demo',
        'mass_mailing',
        'membership',
        'mrp',
        'mrp_byproduct',
        'mrp_repair',
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
        'payment_payumoney',
        'payment_sips',
        'payment_stripe',
        'payment_transfer',
        'point_of_sale',
        'portal',
        'portal_gamification',
        'portal_sale',
        'portal_stock',
        'pos_cache',
        'pos_data_drinks',
        'pos_discount',
        'pos_mercury',
        'pos_reprint',
        'pos_restaurant',
        'procurement',
        'procurement_jit',
        'product',
        'product_email_template',
        'product_expiry',
        'product_extended',
        'product_margin',
        'project',
        'project_issue',
        'project_issue_sheet',
        'purchase',
        'purchase_mrp',
        'purchase_requisition',
        'rating',
        'rating_project',
        'rating_project_issue',
        'report',
        'report_intrastat',
        'resource',
        'sale',
        'sale_crm',
        'sale_expense',
        'sale_margin',
        'sale_mrp',
        'sale_order_dates',
        'sale_service_rating',
        'sales_team',
        'sale_stock',
        'sale_timesheet',
        'stock',
        'stock_account',
        'stock_calendar',
        'stock_dropshipping',
        'stock_landed_costs',
        'stock_picking_wave',
        'subscription',
        'survey',
        'survey_crm',
        'theme_bootswatch',
        'theme_default',
        'utm',
        'web',
        'web_calendar',
        'web_diagram',
        'web_editor',
        'web_kanban',
        'web_kanban_gauge',
        'web_planner',
        'web_settings_dashboard',
        'website',
        'website_blog',
        'website_crm',
        'website_crm_partner_assign',
        'website_customer',
        'website_event',
        'website_event_questions',
        'website_event_sale',
        'website_event_track',
        'website_form',
        'website_forum',
        'website_forum_doc',
        'website_gengo',
        'website_google_map',
        'website_hr',
        'website_hr_recruitment',
        'website_issue',
        'website_links',
        'website_livechat',
        'website_mail',
        'website_mail_channel',
        'website_mass_mailing',
        'website_membership',
        'website_partner',
        'website_payment',
        'website_portal',
        'website_portal_sale',
        'website_project',
        'website_project_issue',
        'website_project_issue_sheet',
        'website_project_timesheet',
        'website_quote',
        'website_rating_project_issue',
        'website_sale',
        'website_sale_delivery',
        'website_sale_digital',
        'website_sale_options',
        'website_sale_stock',
        'website_slides',
        'website_theme_install',
        'website_twitter',
        'web_tour',
    ]

    @api.multi
    def set_color(self, module_dict):
        self.ensure_one()
        module_dict['color'] = 'lightsteelblue'
        module_dict['color_open'] = 'lightyellow'
        if module_dict.get('name') in self._odoo_modules:
            module_dict['color'] = 'yellowgreen'
            module_dict['color_open'] = 'mediumaquamarine'
        return module_dict
