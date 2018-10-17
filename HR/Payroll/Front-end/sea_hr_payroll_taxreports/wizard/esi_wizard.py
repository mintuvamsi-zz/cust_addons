# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _

class PFESIWizard(models.TransientModel):
    _name = 'esi.wizard'

    month_year=fields.Char(string="Month of Year")  

    @api.multi
    def print_esi_report(self):
        data = {}
        data['form'] = self.read(['month_year'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['month_year'])[0])
        return self.env.ref('hr_payroll_taxreports.esi_return_report').report_action(self, data=data)
