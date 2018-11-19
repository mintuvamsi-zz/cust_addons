# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import pdb


class ResConfigSettings(models.TransientModel):
    # _name='timesheet.config.settings'
    _inherit = 'res.config.settings'

    date_validation=fields.Boolean('Date Validation',)
    user_validation=fields.Boolean('User Validation',)
    time_validation=fields.Boolean('Time Validation',)
   # pdb.set_trace()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            #expense_alias_prefix=self.env.ref('hr_expense.mail_alias_expense').alias_name,
            date_validation=self.env['ir.config_parameter'].sudo().get_param('sea_hr_timesheet.date_validation'),
            user_validation=self.env['ir.config_parameter'].sudo().get_param('sea_hr_timesheet.user_validation'),
            time_validation=self.env['ir.config_parameter'].sudo().get_param('sea_hr_timesheet.time_validation'),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        #self.env.ref('hr_expense.mail_alias_expense').write({'alias_name': self.expense_alias_prefix})
        self.env['ir.config_parameter'].sudo().set_param('sea_hr_timesheet.date_validation', self.date_validation)
        self.env['ir.config_parameter'].sudo().set_param('sea_hr_timesheet.user_validation', self.user_validation)
        self.env['ir.config_parameter'].sudo().set_param('sea_hr_timesheet.time_validation', self.time_validation)
