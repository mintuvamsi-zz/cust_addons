from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.tools import float_is_zero, float_compare, pycompat
import re
import pdb


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice','making_charges')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        making_charges = self.making_charges
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else (self.quantity * price) 
        self.price_subtotal=self.price_subtotal+ making_charges
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id.date_invoice).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        #pdb.set_trace()
        self.price_subtotal_signed = price_subtotal_signed * sign

    purity = fields.Selection(related='product_id.product_tmpl_id.purity',string='Purity',store=True)
    wastage = fields.Many2one(related='product_id.product_tmpl_id.wastage',string='Wastage',store=True)
    type_selection = fields.Many2one(related='product_id.product_tmpl_id.type_selection',string='Type',store=True)
    net_weight = fields.Float(related='product_id.product_tmpl_id.net_weight',string='Net Weight',store=True)
    making_charges = fields.Float(related='product_id.product_tmpl_id.making_charges',string='Making Charges',store=True)
    purchased_invoice_no=fields.Char(related='product_id.product_tmpl_id.purchased_invoice_no',string='Purchased Invoice Number',store=True)