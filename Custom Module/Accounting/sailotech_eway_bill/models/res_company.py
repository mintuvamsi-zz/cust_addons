
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from ast import literal_eval
from odoo import api, fields, models
import pdb


class ResCompany(models.Model):
    _inherit = 'res.company'

    app_type=fields.Selection([('withapi','With API'),('withjson','With JSON'),],string = "Application Type Setting",track_visibility='onchange',required=True,)
    clientid=fields.Char(string='Client ID',track_visibility='onchange',required=True)
    client_secret=fields.Char(string='Client Secret',track_visibility='onchange',required=True)

    auth_url=fields.Char(string='Authenticate-URL',track_visibility='onchange',required=True)
    generate_url=fields.Char(string='Genarate-URL',track_visibility='onchange',required=True)
    cancel_url=fields.Char(string='Cancel-URL',track_visibility='onchange',required=True)
    vehicale_update_url=fields.Char(string='Vehical Update-URL',track_visibility='onchange',required=True)
    consolidated_url=fields.Char(string='Consolidated EWB-URL',track_visibility='onchange',required=True)
    



    # @api.onchange('app_type')
    # def _onchange_app_type(self):
    #     if self.app_type == "withapi":
    #         self.update({
    #             'group_show_with_json': False,
    #             'group_show_with_api': True,
    #         })
    #     else:
    #         self.update({
    #             'group_show_with_json': True,
    #             'group_show_with_api': False,
    #         })




    # @api.model
    # def get_values(self):
    #     print("Inside config get_values *****************")
    #     res = super(ResCompany, self).get_values()
    #     ICPSudo = self.env['ir.config_parameter'].sudo()
        
    #     res.update(
    #         with_api=ICPSudo.get_param('app_type', default=False),
    #         clientid=ICPSudo.get_param('clientid', default=False),
    #         client_secret=ICPSudo.get_param('client_secret', default=False),
    #         )
    #     return res

    # @api.multi
    # def set_values(self):
    #     print("Inside config set_values *****************")
    #     super(ResCompany, self).set_values()
    #     ICPSudo = self.env['ir.config_parameter'].sudo()
        
    #     ICPSudo.set_param("eway.bill..app_type", self.app_type)
    #     ICPSudo.set_param('eway.bill.clientid', self.clientid)
    #     ICPSudo.set_param('eway.bill.client_secret', self.client_secret)
    #     print("Inside the Config Setting**********************")
    #     # pdb.set_trace()
