
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.tools import float_is_zero, float_compare, pycompat
import re
import pdb


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    purity = fields.Selection(related='product_id.product_tmpl_id.purity',string='Purity',store=True)
    wastage = fields.Many2one(related='product_id.product_tmpl_id.wastage',string='Wastage',store=True)
    type_selection = fields.Many2one(related='product_id.product_tmpl_id.type_selection',string='Type',store=True)
    net_weight = fields.Float(related='product_id.product_tmpl_id.net_weight',string='Net Weight',store=True)
    making_charges = fields.Float(related='product_id.product_tmpl_id.making_charges',string='Making Charges',store=True)
    purchased_invoice_no=fields.Char(related='product_id.product_tmpl_id.purchased_invoice_no',string='Purchased Invoice Number',store=True)

    # karat = fields.Selection([
    #     ('22k', '22K'),
    #     ('24k', '24K'),], string='Karat')
    #making_charges=fields.Float('Making Charges')
    #