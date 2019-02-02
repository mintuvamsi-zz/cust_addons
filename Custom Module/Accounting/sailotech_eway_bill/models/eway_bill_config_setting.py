
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import pdb


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    with_api=fields.Boolean(string='With Api',)

    @api.model
    def get_values(self):
        print("Inside config get_values *****************")
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        
        res.update(with_api=ICPSudo.get_param('with_api', default=False),)
        return res

    @api.multi
    def set_values(self):
        print("Inside config set_values *****************")
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        
        ICPSudo.set_param("with_api", self.with_api)
        print("Inside the Config Setting**********************")
        # pdb.set_trace()