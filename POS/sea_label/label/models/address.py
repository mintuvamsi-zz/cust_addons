# -*- coding: utf-8 -*-
from odoo import models, api, _

class address(models.Model):
    _inherit = "product.template"

    partner_id = fields.Many2one(
        'res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get())

    # street_name = fields.Char('Street Name', compute='_compute_address',
    #                           inverse='_inverse_street_name')
    # street_number = fields.Char('House Number', compute='_compute_address',
    #                             inverse='_inverse_street_number')
    # street_number2 = fields.ChFar('Door Number', compute='_compute_address',
    #                              inverse='_inverse_street_number2')
    #
    # def _get_company_address_fields(self, partner):
    #     address_fields = super(Company, self)._get_company_address_fields(partner)
    #     address_fields.update({
    #         'street_name': partner.street_name,
    #         'street_number': partner.street_number,
    #         'street_number2': partner.street_number2,
    #     })
    #     return address_fields