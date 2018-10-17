# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.addons import decimal_precision as dp
import pdb

class ProductTemplate(models.Model):
    _inherit = "product.template"
   
    _description = "Product Inherit"
    

    name = fields.Char('Order Reference', required=True, index=True, copy=False, default='New')
    sp_total=fields.Float('Total')
    cp_total=fields.Float('Total')
    sp_tax_selection = fields.Selection([
        ('Inclusive', 'Inclusive'),
        ('Exclusive', 'Exclusive'),
        
        ], string='SP Tax', store=True, copy=False,)
    sp_tax_value=fields.Float('Tax Amount')

    cp_tax_selection = fields.Selection([
        ('Inclusive', 'Inclusive'),
        ('Exclusive', 'Exclusive'),
        
        ], string='CP Tax', store=True, copy=False,)
    cp_tax_value=fields.Float('Tax Amount')

    eligibility=fields.Float('Eligibility (%)')

    eligibility_type=fields.Selection([('Input Goods', 'Input Goods'),
        ('Input Capital Goods', 'Input Capital Goods'),('Input Services','Input Services')
        
        ], string='Eligibility Type', store=True, copy=False,)

    
    
    @api.onchange('sp_tax_selection','sp_total')
    def on_change_list_price(self):
        #pdb.set_trace()
        result = []
        if self.sp_total:
            if self.taxes_id and self.list_price:
                children_tax_ids=self.taxes_id[0].children_tax_ids
                tax_amount=0
                sale_price=self.sp_total
                for tax in children_tax_ids:
                    tax_amount=tax.amount+tax_amount
                if self.sp_tax_selection=='Inclusive':
                    
                    self.list_price=(sale_price/(100+tax_amount))*100
                    self.sp_tax_value=(sale_price/(100+tax_amount))*tax_amount
                if self.sp_tax_selection=='Exclusive':
                   # sale_price=self.list_price
                    self.list_price=sale_price
                    self.sp_tax_value=(sale_price*(tax_amount/100))

    
    @api.onchange('cp_tax_selection','cp_total')
    def on_change_standard_price(self):
        #pdb.set_trace()
        result = []
        if self.cp_total:
            if self.supplier_taxes_id and self.standard_price:
                children_tax_ids=self.supplier_taxes_id[0].children_tax_ids
                tax_amount=0
                cost_price=self.cp_total
                for tax in children_tax_ids:
                    tax_amount=tax.amount+tax_amount
                if self.cp_tax_selection=='Inclusive':
                    
                    self.standard_price=(cost_price/(100+tax_amount))*100
                    self.cp_tax_value=(cost_price/(100+tax_amount))*tax_amount
                if self.cp_tax_selection=='Exclusive':
                    #cost_price=self.standard_price
                    self.standard_price=cost_price
                    self.cp_tax_value=(cost_price*(tax_amount/100))



        

