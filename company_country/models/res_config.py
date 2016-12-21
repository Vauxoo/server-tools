# -*- coding: utf-8 -*-
# Copyright 2016 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import os

from openerp import api, exceptions, models


class CountryCompanyConfigSettings(models.TransientModel):
    _name = 'country.company.config.settings'

    @api.model
    def load_country_company(self, country_code=None):
        if not country_code:
            country_code = os.environ.get('COUNTRY')
        if not country_code:
            raise exceptions.ValidationError(
                'Error COUNTRY environment variable with country code '
                'not defined')
        country = self.env['res.country'].search([
            ('code', 'ilike', country_code)], limit=1)
        if not country:
            raise exceptions.ValidationError(
                'Country code %s not found. Use ISO 3166 codes 2 letters')
        self.env.ref('base.main_company').write({'country_id': country.id})
