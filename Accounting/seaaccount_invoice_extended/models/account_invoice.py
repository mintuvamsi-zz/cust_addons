from odoo import api, fields, models
class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    standard_cost = fields.Float(related="product_id.lst_price", readonly=True, string='Sale Price')
    barcode=fields.Char(related="product_id.barcode", readonly=True, string='BarCode')