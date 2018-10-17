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
import re

class ProductTemplate(models.Model):
    _inherit = "product.template"
   
    _description = "Product Inherit"



    

    # name = fields.Char('Order Reference', required=True, index=True, copy=False, default='New')
    # sp_total=fields.Float('Total')
    # cp_total=fields.Float('Total')
    purity = fields.Selection([
        ('916', '916'),], string='Purity')
    making_charges=fields.Float('Making Charges')
    net_weight=fields.Float('Net Weight')

    wastage = fields.Many2one('product.template.wastage','Wastage')
    type_selection = fields.Many2one('daily.price','Type')
    product_identification=fields.Char('Product Identification')
    serial_sequence=fields.Char('Serial Sequence')
    purchased_invoice_no=fields.Char('Purchased Invoice Number')
    active_serial_num = fields.Boolean(related='company_id.active_serial_num',string='Active Serial Number',store=True)
    

    @api.multi
    def cost_price_updt(self):
        #pdb.set_trace()
        context = dict(self._context or {})
        #active_ids = context.get('active_id', []) or []
        product_template_id=self.id
        #company_id=product_template.browse(active_ids).company_id.id
        #quantity=self.quantity
        #user_id=product_template.browse(active_ids).create_uid.id
        # conn_string = "host='localhost' dbname='Jew' user='karthik' password='odoo'"
        # conn = psycopg2.connect(conn_string)
        # conn.rollback()
        # cursor = conn.cursor()
        
        #end_date=str(self.date_to)
        #cursor.rollback()
        self._cr.execute("SELECT * FROM cost_price_updt("+str(product_template_id)+")")
        #status=cursor.fetchone()[0]
        #records = cursor.fetchall()
        # get_invoices=self.env['account.invoice'].search([('invoice_status','=','Ready to transffer'),('date_invoice','>=',self.date_from),('date_invoice','<=',self.date_to)])
        # start_date=self.date_from
        # end_date=self.date_to
        # period=self.period
        # gst_in=self.gst_in
        # p_user=self.p_user
        # query_string="select * from test_insert("+"'"+str(gst_in)+"','"+str(start_date)+"','"+str(end_date)+"','"+str(period)+"','"+str(p_user)+"')"
        # self.env.cr.execute(query_string)
        self.env.cr.commit()






    # cp_tax_value=fields.Float('Tax Amount')

    # eligibility=fields.Float(string='Eligibility (%)', default=100.0)

    # eligibility_type=fields.Selection([('ip', 'Input Goods'),
    #     ('cp', 'Input Capital Goods'),('is','Input Services'),('no','NO')
        
    #     ], string='Eligibility Type', store=True, copy=False,)

class ProductTemplateWastage(models.Model):
    _name = "product.template.wastage"
    _rec_name ='wastage'
   
    _description = "Product Inherit Extended for Wastage"

    wastage = fields.Char(string='Wastage')
    #type_selection = fields.Char('Type')
    # @api.onchange('eligibility_type')
    # def onchange_eligibility_type(self):
    #     if self.eligibility_type =='no':
    #         self.eligibility=0
    #     else:
    #         self.eligibility=100.0


# class ProductTemplateType(models.Model):
#     _name = "product.template.type"
#     _rec_name ='type_selection'
   
#     _description = "Product Inherit Extended for Type"

#     type_selection = fields.Char(string='Type')

#     @api.onchange('sp_tax_selection')
#     def onchange_selection(self):
#         self.list_price=0
#         self.sp_tax_value=0
#         self.sp_total=0
#     @api.onchange('cp_tax_selection')
#     def onchange_cp_selection(self):
#         self.standard_price=0
#         self.cp_total=0
#         self.cp_tax_value=0
    
#     @api.onchange('sp_total','list_price')
#     def on_change_list_price(self):
#         #pdb.set_trace()
#         result = []
#         if self.sp_tax_selection=='Inclusive':
#             self.sale_price=0
#             self.sp_tax_value=0
#             if self.sp_total:
#                 children_tax_ids=self.taxes_id[0].children_tax_ids
#                 tax_amount=0
#                 sale_price=self.sp_total
#                 for tax in children_tax_ids:
#                     tax_amount=tax.amount+tax_amount
#                 self.list_price=(sale_price/(100+tax_amount))*100
#                 self.sp_tax_value=(sale_price/(100+tax_amount))*tax_amount
#         if self.sp_tax_selection=="Exclusive":
#             self.sp_tax_value=0
#             self.sp_total=0
#             if self.list_price:
#                 children_tax_ids=self.taxes_id[0].children_tax_ids
#                 tax_amount=0
#                 sale_price=self.sp_total
#                 for tax in children_tax_ids:
#                     tax_amount=tax.amount+tax_amount
#                 self.sp_tax_value=(self.list_price*(tax_amount/100))
#                 self.sp_total=self.list_price+self.sp_tax_value

    
#     @api.onchange('standard_price','cp_total')
#     def on_change_standard_price(self):
#         #pdb.set_trace()
#         result = []
#         if self.cp_tax_selection=='Inclusive':
#             if self.cp_total:
#                 children_tax_ids=self.supplier_taxes_id[0].children_tax_ids
#                 tax_amount=0
#                 cost_price=self.cp_total
#                 for tax in children_tax_ids:
#                     tax_amount=tax.amount+tax_amount
#                 self.standard_price=(cost_price/(100+tax_amount))*100
#                 self.cp_tax_value=(cost_price/(100+tax_amount))*tax_amount
#         if self.cp_tax_selection=="Exclusive":
#             if self.standard_price:
#                 children_tax_ids=self.supplier_taxes_id[0].children_tax_ids
#                 tax_amount=0
                
#                 for tax in children_tax_ids:
#                     tax_amount=tax.amount+tax_amount
                
#                 self.cp_tax_value=(self.standard_price/(100+tax_amount))*tax_amount
#                 self.cp_total=self.standard_price+self.cp_tax_value


    
#     # @api.constrains('list_price')
#     # @api.one
#     # def _check_values_sales(self):
#     #     if (self.list_price<=0.0):
#     #         raise Warning(_('Zero Values are not allowed for Sales Price...!'))


#     # @api.constrains('standard_price')
#     # @api.one
#     # def _check_values_cost(self):
#     #     if (self.standard_price == 0.00):
#     #         raise Warning(_('Zero Values are not allowed for Cost Price...!'))
#     # #     # elif (self.standard_price<=0.00):
#     # #     #     raise Warning(_('Zero Values are not allowed for Cost Price...!'))

        
#     # #constraint
#     # @api.constrains('l10n_in_hsn_code')
#     # @api.one
#     # def _check_hsn(self):
#     #     l10n_in_hsn_code = self.l10n_in_hsn_code
#     #     if l10n_in_hsn_code and len(str(l10n_in_hsn_code)) > 8:
#     #         list_of_speacial=['^','~','+','&','@','(','[','!','#','$','%',']','*',')','$','/',',','.','-','_','=',':',';','"',"'"]
#     #         for char  in self.l10n_in_hsn_code:
#     #             if char in list_of_speacial:
#     #                 raise Warning(_('HSN/SAC code should not exced 8 digits and special charectors are not allowed...!'))



#     #constraint
#     @api.constrains('l10n_in_hsn_code')
#     @api.one
#     def _check_hsn(self):
#         l10n_in_hsn_code = self.l10n_in_hsn_code
#         list_of_speacial=['^','~','+','&','@','(','[','!','#','$','%',']','*',')','$','/',',','.','-','_','=',':',';','"',"'"]
#         if len(str(l10n_in_hsn_code)) > 8:
#             raise Warning(_('HSN/SAC code should not exced 8 digits...!'))
#         elif re.match("^[a-z]*$",l10n_in_hsn_code):
#             raise Warning(_('HSN/SAC code should not contain Alphabates...!'))
#         for char  in self.l10n_in_hsn_code:
#             if char in list_of_speacial:
#                 raise Warning(_('HSN/SAC code should not contain special charectors...!'))


# class Product_Uom(models.Model):
#     _inherit="product.uom"
#     ucq=fields.Char('UQC')