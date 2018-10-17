# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class WizardB2cs(models.TransientModel):
    _name = 'wizard.b2cs'

    start_date = fields.Date('From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Date('To Date', default=fields.Datetime.now(), required=True)

    @api.multi
    def print_b2cs_report(self):
        data = {}
        data['form'] = self.read(['start_date','end_date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['start_date','end_date'])[0])
        return self.env.ref('india_gst.gstr_b2cs_report').report_action(self, data=data)
