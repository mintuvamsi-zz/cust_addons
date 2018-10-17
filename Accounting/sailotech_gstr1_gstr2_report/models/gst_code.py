# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CountryState(models.Model):
    _description = "Country state"
    _inherit = 'res.country.state'

    state_code = fields.Char('Code', help='Numeric State Code ')

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    _name = "account.invoice"

    elec_ref = fields.Char('Electronic Reference')
    ship_bill_date = fields.Date('Shipping Bill Date')
    ship_bill_no = fields.Char('Shipping Bill No.')
    port_code = fields.Many2one('port.code')
    export_invoice = fields.Boolean('Export Invoice')
    export_type = fields.Selection([('WPAY','WPAY'),('WOPAY','WOPAY')])
    invoice_type=fields.Selection([('Regular','Regular'),('SEZ supplies with payment','SEZ supplies with payment'),('SEZ supplies without payment','SEZ supplies without payment'),
                                  ('Deemed Export','Deemed Export')],string="Invoice Type",default='Regular',required=True)

    def get_gst(self,inv_id,product_id):
        invoice = self.search([('id','=',inv_id)],limit=1)
        tax_amount = 0
        rate = 0

        for num in invoice.invoice_line_ids:
            if num.product_id.id == product_id:

                tax_rate = 0
                for i in num.invoice_line_tax_ids:

                    if i.children_tax_ids:
                        tax_rate = sum(i.children_tax_ids.mapped('amount'))

                tax_amount = ((tax_rate/100)*num.price_subtotal)/2
                rate = tax_rate/2
        return [rate,tax_amount]


    def get_igst(self,inv_id,product_id):
        invoice = self.search([('id','=',inv_id)],limit=1)
        tax_amount = 0
        rate = 0
        for i in invoice.invoice_line_ids:
            if i.product_id.id == product_id:
                tax_rate = 0
                for t in i.invoice_line_tax_ids:
                    if not t.children_tax_ids:
                        tax_rate = t.amount
                tax_amount = (tax_rate/100)*i.price_subtotal
                rate = tax_rate
        return [rate,tax_amount]


class PortCode(models.Model):
    _name = 'port.code'

    name = fields.Char('Port Name')
    code = fields.Char('Port Code')

