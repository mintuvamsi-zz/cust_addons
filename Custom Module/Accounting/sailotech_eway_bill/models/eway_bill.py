# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from datetime import datetime,timedelta,time
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError, AccessError
import re
import time
from string import *
import pdb
import json
import base64
import requests

class SailotechEwayBill(models.Model):
    _name = 'eway.bill'
    _rec_name='eway_bill_no'
    _inherit = ['mail.thread','base',]


    # @api.multi
    # def _default_gstin(self):
    #     gstin=res.company
    #     return from_name


    # @api.multi
    # def _default_from_place(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     place=eway_bill_no.browse(active_ids).to_name.state_id.name
    #     return place
    

    @api.one
    @api.depends('ewaybill_item_id.price_total', 'ewaybill_item_id.tax_amount', 'ewaybill_item_id.cgst',
                 'ewaybill_item_id.igst', 'ewaybill_item_id.sgst', 'ewaybill_item_id.cess', )
    def _compute_amount(self):
        # pdb.set_trace()
        self.amount_tax = sum((line.tax_amount) for line in self.ewaybill_item_id)
        self.amount_untaxed = sum(line.price_total for line in self.ewaybill_item_id)-self.amount_tax
        self.amount_total = self.amount_untaxed + self.amount_tax
        self.igst_total= sum((line.igst) for line in self.ewaybill_item_id)
        self.cgst_total= sum((line.cgst) for line in self.ewaybill_item_id)
        self.sgst_total= sum((line.sgst) for line in self.ewaybill_item_id)
        self.cess_total= sum((line.cess) for line in self.ewaybill_item_id)

    # from_name=fields.Many2one('res.company',string='From Name',required=True,index=True, default=lambda self: self.env.user.company_id.id)
    
    # from_name=fields.Many2one('res.partner',string='From Name',required=True)
    from_name = fields.Many2one('res.company', 'Company Name', default=lambda self: self.env['res.company']._company_default_get('eway.bill'))
    gstin=fields.Char(string='Company GSTIN',required=True)
    bill_status=fields.Selection([('active','Active'),('in_active','Inactive'),],default='active',string = "E-Way Bill Status",track_visibility='onchange')
    transaction_type=fields.Selection([('I','Inward'),('O','Outward'),],default='O',string = "Transaction Type",track_visibility='onchange',required=True)
    sub_type=fields.Selection([('1','Supply'),('2','Import'),('3','Export'),('4','Job work'),('5','For Own Use'),('6','Job work Returns'),('7','Sales Returns'),('8','thers'),('9','SKD/CKD'),('10','Line Sales'),('11','Recipint Not Known'),('12','Exhibition or Fairs'),],default='1',string = "Sub Type",track_visibility='onchange',required=True)
    doc_type=fields.Selection([('INV','Invoice'),('BIL','Bill'),('BOE','Bill of Entry'),('CHL','Delivery Challan'),('CTN','Credit Note'),('OTH','Others'),],default='INV',string = "Document Type",track_visibility='onchange',required=True)
    doc_no=fields.Char(string='Document No',track_visibility='onchange',required=True)
    doc_date=fields.Date(string='Document Date',track_visibility='onchange',required=True)
    # from_place=fields.Char(string='From Place',default=_default_from_place)
    to_name=fields.Many2one('res.partner',string='To Name',required=True)
    to_gstin=fields.Char(string='To GSTIN', track_visibility='onchange',required=True)
    to_add=fields.Char(string='Shipping Address', track_visibility='onchange',required=True)
    to_add1=fields.Char(track_visibility='onchange',required=True)
    to_state=fields.Char(string='To State', track_visibility='onchange',required=True)
    
    
    transport_mode=fields.Selection([('1','Road'),('2','Rail'),('3','Air'),('4','Ship'),],default='1',string = "Mode",track_visibility='onchange',required=True)
    transporter_name=fields.Char(string='Transporter Name', track_visibility='onchange',)
    transporter_id=fields.Char(string='Transporter ID',track_visibility='onchange',)
    transport_doc_no=fields.Char(string='Transporter Doc No',track_visibility='onchange',)
    transport_doc_date=fields.Date(string='Transporter Doc Date',track_visibility='onchange',)
    transport_distance=fields.Integer(string='Distance(Km)',track_visibility='onchange',)
    veh_valid_from=fields.Datetime(string='Vehicle Details Valid From',track_visibility='onchange')
    veh_valid_upto=fields.Datetime(string='Vehicle Details Valid Upto',track_visibility='onchange')
    vehicle_no=fields.Char(string='Vehicle No',track_visibility='onchange', )
    vehicle_type=fields.Selection([('R','Regular'),('O','Ordinery'),],default='R',string = "Vehicle Type",track_visibility='onchange',)
    eway_bill_no=fields.Char(string='E-Way Bill No',track_visibility='onchange',)
    eway_bill_date=fields.Datetime(string='E-Way Bill Date',track_visibility='onchange',)
    valid_date=fields.Datetime(string='E-Way Bill Valid Upto',track_visibility='onchange',)
    tokan_gen_time=fields.Datetime(string='Token Generation Time',track_visibility='onchange',)
    status=fields.Selection([('draft','Draft'),('active','Active'),('inactive','Inactive'),('cancel','Cancel'),],string = "Status",track_visibility='onchange',default='draft')

    amount_untaxed = fields.Float(string='Untaxed Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_tax = fields.Float(string='Tax',
        store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Float(string='Total',
        store=True, readonly=True, compute='_compute_amount')
    igst_total=fields.Float(string='IGST Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    cgst_total=fields.Float(string='CGST Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    sgst_total=fields.Float(string='SGST Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    cess_total=fields.Float(string='CESS Amount',
        store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    ewaybill_item_id=fields.One2many('eway.bill.items','eway_bill_id',string='E-Way Bill Item')
    history_id=fields.One2many('eway.bill.history','eway_bill_history_id',string='E-Way Bill History')
    vehicle_history_id=fields.One2many('eway.bill.vehicle.history','vehicle_no_history_id',string='Vehicle History')


    @api.multi
    @api.onchange('from_name') 
    def on_change_from_company_id(self):
      if self.from_name:
        # pdb.set_trace()
        self.gstin=self.from_name.vat



    @api.multi
    @api.onchange('to_name') 
    def on_change_company_id(self):
        res= {}
        company_list= []
        if self.to_name:
            # pdb.set_trace()
            self.to_gstin=self.to_name.vat

            res_partner_obj= self.env['res.partner']
            child_comapny_ids=res_partner_obj.search([('parent_id','=', self.to_name.id)])
            self.to_add=child_comapny_ids.street
            self.to_add1=child_comapny_ids.street2
            self.to_state=child_comapny_ids.state_id.name
            for record in child_comapny_ids:
                company_list.append(record.id)
            company_list.append(self.to_name.id)
        res= {'domain':{'partner_shipping_id':[('id','in',company_list)]}}
        # pdb.set_trace()
        return res
        


    @api.constrains('doc_date')
    @api.multi
    def _check_doc_date(self):
        if not self.doc_date:
            raise Warning(_('Please Enter Doc Date...!'))

    @api.constrains('transport_doc_date')
    @api.multi
    def _check_transport_doc_date_len(self):
        # if not self.transport_doc_date:
        #     raise Warning(_('Please Enter Transporter Doc Date...!'))
        # print("in _check_transport_doc_date_len************")
        # # pdb.set_trace()
        if self.transport_doc_date:
            dt=datetime.now()
            dstr=dt.strftime("%Y-%m-%d")
            newdate1 = time.strptime(dstr, "%Y-%m-%d")
            newdate2 = time.strptime(self.transport_doc_date, "%Y-%m-%d")
            # pdb.set_trace()
            if newdate2 > newdate1:
                raise Warning(_('Transporter Doc Date should not be more than today...!'))


    @api.constrains('transport_distance')
    @api.multi
    def _check_transport_distance(self):
        # pdb.set_trace()
        if self.transport_distance:
            if self.transport_distance>999:
                raise Warning(_('Transportation Distance should not be more than 999 Km...!'))
        elif not self.transport_distance:
            raise Warning(_('Please Enter Transportation Distance...!'))

    @api.constrains('vehicle_no')
    @api.multi
    def _check_vehicle_no(self):
        if self.vehicle_no:
            if len(self.vehicle_no)>10:
                raise Warning(_('Improper Vehicle No, It should not be more than 10 digits...!'))
        elif not self.vehicle_no:
            raise Warning(_('Please Enter Vehicle No...!'))


    @api.constrains('transport_doc_date')
    @api.multi
    def _check_transport_doc_date(self):
        # pdb.set_trace()
        if self.doc_date and self.transport_doc_date:
            newdate1 = time.strptime(self.doc_date, "%Y-%m-%d")
            newdate2 = time.strptime(self.transport_doc_date, "%Y-%m-%d")
            if newdate1 > newdate2:
                raise Warning(_('Transporter document date cannot be earlier than the Invoice Date(Document Date)...!'))


    #constraint
    @api.constrains('gstin')
    @api.one
    def _check_gstin(self):
        gstin_num = self.gstin
        list_of_special=['^','~','+','&','@','(','[','!','#','$','%',']','*',')','$','/',',','.','-','_','=',':',';','"',"'"]
        alpha=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        if (len(str(gstin_num)) > 15):
            raise Warning(_('GSTIN No should not more than 15 charectors...!'))

        if (len(str(gstin_num)) != 0) and (len(str(gstin_num)) < 15):
            raise Warning(_('GSTIN No should not less than 15 digits...!'))

        if len(str(gstin_num))==15:
            if (len(str(gstin_num)) == 15):
                for char  in gstin_num:
                    if char in list_of_special:
                        raise Warning(_('GSTIN No should not contain Special Charectors...!'))
                for char  in gstin_num:
                    if char in alpha:
                        raise Warning(_('GSTIN No should not contain Lowercase Alphabates...!'))


    #constraint
    @api.constrains('to_gstin')
    @api.one
    def _check_to_gstin(self):
        gstin_num = self.to_gstin
        list_of_special=['^','~','+','&','@','(','[','!','#','$','%',']','*',')','$','/',',','.','-','_','=',':',';','"',"'"]
        alpha=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        if (len(str(gstin_num)) > 15):
            raise Warning(_('GSTIN No should not more than 15 charectors...!'))

        if (len(str(gstin_num)) != 0) and (len(str(gstin_num)) < 15):
            raise Warning(_('GSTIN No should not less than 15 digits...!'))

        if len(str(gstin_num))==15:
            if (len(str(gstin_num)) == 15):
                for char  in gstin_num:
                    if char in list_of_special:
                        raise Warning(_('GSTIN No should not contain Special Charectors...!'))
                for char  in gstin_num:
                    if char in alpha:
                        raise Warning(_('GSTIN No should not contain Lowercase Alphabates...!'))



    @api.multi      
    def auth(self):
        # defining the api-endpoint
        API_ENDPOINT = "https://aspone.in/api/ewaybills/authenticate"
        headers = {'content-type': 'application/json', 'accept': 'application/json',
                'username': 'test_dlr222',
                'password':'test_dlr222',
                'gstin':self.from_name.vat,
                'clientid':'snf3f9e69dfa0b76b12',
                'client-secret':'snfa6e36f63adad4db0'}
        
        r = requests.post(url = API_ENDPOINT,headers=headers)
        self.tokan_gen_time=datetime.now()

        auth_token = r.text
        print("The pastebin URL is:%s"%auth_token)


    @api.multi
    def generate_eway_bill(self):
        filename= 'generate_eway_bill.json'
        item_list=[]
        # pdb.set_trace()
        if self.tokan_gen_time:
            d1=datetime.strptime(self.tokan_gen_time, "%Y-%m-%d %H:%M:%S")
            d1_ts = time.mktime(d1.timetuple())
            d2=datetime.now()
            print("Before if condition****************")
            d2_ts = time.mktime(d2.timetuple())
            if (int(d2_ts-d1_ts) / 60) >360:
                # pdb.set_trace()
                print("Inside if condition****************")
                self.auth()
        if not self.tokan_gen_time:
            self.auth()
        # pdb.set_trace()
        dt=self.doc_date
        dat=datetime.strptime(dt, '%Y-%m-%d').strftime('%d/%m/%Y')

        if self.transport_doc_date:
            tdd=self.transport_doc_date
            tra_doc_dat=datetime.strptime(tdd, '%Y-%m-%d').strftime('%d/%m/%Y')
        else:
            tra_doc_dat=''

        for product in self.ewaybill_item_id:
            res={}


            res["ProductName"]=str(product.product_id.name)
            res["ProductDesc"]=product.description[0]
            res["HsnCode"]=product.hsn
            res["Quantity"]=product.quantity
            res["QtyUnit"]="KGS"
            res["CgstRate"]=product.cgst1
            res["SgstRate"]=product.sgst1
            res["IgstRate"]=product.igst1
            res["CessRate"]=product.cess1
            res["CessAdvol"]=0
            res["TaxableAmount"]=product.tax_amount
            item_list.append(res)

        data={
        "eway_bill": 
        { 
        "SupplyType":self.transaction_type,
        "SubSupplyType":self.sub_type,
        "DocType":self.doc_type,
        "DocNo":self.doc_no,
        "DocDate":dat,
        "FromGstin":self.from_name.vat,
        "FromTrdName":self.from_name.name,
        "FromAddr1":self.from_name.street,
        "FromAddr2":self.from_name.street2,
        "FromPlace":str(self.from_name.city),
        "FromPincode":(self.from_name.zip),
        "FromStateCode":int(self.from_name.state_id.l10n_in_tin),
        "ToGstin":self.to_name.vat,
        "ToTrdName":self.to_name.name,
        "ToAddr1":self.to_name.street,
        "ToAddr2":self.to_name.street2,
        "ToPlace":str(self.to_name.city),
        "ToPincode":(self.to_name.zip),
        "ToStateCode":int(self.to_name.state_id.l10n_in_tin),
        "TotalValue":self.amount_total,
        "CgstValue":self.cgst_total,
        "SgstValue":self.sgst_total,
        "IgstValue":self.igst_total,
        "CessValue":self.cess_total,
        "TransporterId":self.transporter_id,
        "TransporterName":self.transporter_name,
        "TransDocNo":self.transport_doc_no,
        "TransMode":self.transport_mode,
        "TransDistance":str(self.transport_distance),
        "TransDocDate":tra_doc_dat,
        "VehicleType":self.vehicle_type,
        "VehicleNo":self.vehicle_no,
        "ItemList":item_list}}
        
        # -------------------------------------------------------------------
        API_ENDPOINT = "https://aspone.in/api/ewaybills/generate_eway_bill"
        # API_ENDPOINT = self.from_name.generate_url
        headers = {'content-type': 'application/json', 'accept': 'application/json',
                  'gstin':self.from_name.vat,
                  'clientid':'snf3f9e69dfa0b76b12',
                  'client-secret':'snfa6e36f63adad4db0'}
        # ----------------------------------------------------
        # context = dict(self._context or {})
        # active_ids = context.get('active_id', []) or []
        # conf=self.env['res.company']
        app_type=self.from_name.app_type
        print("Inside generate fun before PDB*****************")
        # pdb.set_trace()
        # -----------------------------------------------------
        # sending post request and saving response as response object
        if app_type=="withapi":
            print("********************Inside generate before API call*********************")
            r = requests.post(url = API_ENDPOINT,headers=headers,data=json.dumps(data))
            print("1st Request for Generation inside With API****************")
            # pdb.set_trace()
            ewbno={}
            ewbno = r.text
            self.status='active'
            print("*********************%s"%ewbno)
            
            if self.eway_bill_no:
                self.env['eway.bill.history'].create({
                    'eway_bill_no':self.eway_bill_no,
                    'eway_bill_date':self.eway_bill_date,
                    'valid_date':self.valid_date,  
                    'eway_bill_history_id':self.id           
                    })
            if ewbno:
                if ewbno.find("errorCodes") > 0:
                    raise UserError(_('There is an error in the application:%s'%ewbno))
                elif ewbno.find("ewayBillNo"):
                    self.eway_bill_no=json.loads(ewbno).get('ewayBillNo')
                    date=json.loads(ewbno).get('ewayBillDate')
                    dates=datetime.strptime(date[0:19], "%d/%m/%Y %H:%M:%S")
                    self.eway_bill_date=dates.strftime("%Y-%m-%d %H:%M:%S")

                    valid=json.loads(ewbno).get('validUpto')
                    v_dates=datetime.strptime(valid[0:19], "%d/%m/%Y %H:%M:%S")
                    self.valid_date=v_dates.strftime("%Y-%m-%d %H:%M:%S")


            
            
            print("The pastebin URL is:%s"%ewbno)

        # --------------------------------------------------------------------


        if app_type=="withjson":
            print("Inside the If check concition With JSON*****************")
            d=json.dumps(data, indent=4)
            b = bytes(d, 'utf-8')
            export_id = self.env['excel.extended'].create({'excel_file': base64.encodestring(b), 'file_name': filename})
            print("end of If check****************")
            return{
                'view_mode': 'form',
                'res_id': export_id.id,
                'res_model': 'excel.extended',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                # 'context': context,
                'target': 'new', }
        # --------------------------------------------------------------------

    @api.multi
    def cancel_eway_bill(self):

        d1=datetime.strptime(self.tokan_gen_time, "%Y-%m-%d %H:%M:%S")
        d1_ts = time.mktime(d1.timetuple())
        d2=datetime.now()
        print("Before if condition****************")
        d2_ts = time.mktime(d2.timetuple())
        if (int(d2_ts-d1_ts) / 60) >360:
            # pdb.set_trace()
            print("Inside if condition****************")
            self.auth()

        # defining the api-endpoint
        API_ENDPOINT = "https://aspone.in/api/ewaybills/cancel_eway_bill"
        # API_ENDPOINT = self.from_name.cancel_url
        headers = {'content-type': 'application/json',
                   'accept': 'application/json',
                   'gstin':self.from_name.vat,
                   'clientid':'snf3f9e69dfa0b76b12',
                   'client-secret':'snfa6e36f63adad4db0'}
        
        data = {
            "eway_bill":{
                "ewbNo":self.eway_bill_no,
                "cancelRsnCode": 2,
                "cancelRmrk": "Cancelled the order"
                }
            }

        r = requests.post(url = API_ENDPOINT,headers=headers,data=json.dumps(data))
        self.status='cancel'
        pastebin_url = r.text
        print("The pastebin URL is:%s"%pastebin_url)



class inventory_excel_extended(models.Model):
    _name= "excel.extended"
    

    excel_file = fields.Binary('Dowload Report Excel')
    file_name = fields.Char('Excel File', size=64)


class EwayBillItems(models.Model):
    _name = 'eway.bill.items'


    product_id=fields.Many2one('product.product', string='Product Name',track_visibility='onchange')
    description=fields.Char(string='Description',track_visibility='onchange')
    hsn=fields.Char(related='product_id.product_tmpl_id.l10n_in_hsn_code', string='HSN Code', store=True , readonly=True)
    quantity=fields.Integer(string='Quantity',track_visibility='onchange')
    # product_uom = fields.Many2one('product.uom', string='Product Unit of Measure', required=True)

    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))

    price_total = fields.Float(string='Total', store=True)
    # price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)
    tax_amount=fields.Float(string="Tax Amount")
    uom=fields.Char(string="Unit of Measure")

    cess1=fields.Float('CESS(%)')
    igst1=fields.Float('IGST(%)')
    sgst1=fields.Float('SGST(%)')
    cgst1=fields.Float('CGST(%)')

    cess=fields.Float('CESS')
    igst=fields.Float('IGST')
    sgst=fields.Float('SGST')
    cgst=fields.Float('CGST')

    taxes_id = fields.Many2one('account.tax', string='Taxes', )
    eway_bill_id=fields.Many2one('eway.bill',string='E-Way bill ID')

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if self.product_id:
            if self.product_id.name_get()[0][1] and self.product_id.description_sale:
                self.description=self.product_id.name_get()[0][1]+self.product_id.description_sale
            if self.product_id.description_sale:
                self.description=self.product_id.description_sale
            if self.product_id.name_get()[0][1]:
                self.description=self.product_id.name_get()[0][1]
            # pdb.set_trace()
            self.price_unit=self.product_id.list_price
            if self.product_id.uom_id:
                self.uom=self.product_id.uom_id.name
    

    @api.multi
    @api.onchange('price_unit','quantity','taxes_id')
    def onchange_toatal(self):
        if self.quantity and self.price_unit:
            self.price_total=self.quantity*self.price_unit
            # pdb.set_trace()
            if self.taxes_id:
                tax_amount=0
                amount=0
                cess_amount=0

                
                for tax_id in self.taxes_id:

                    if tax_id.children_tax_ids:
                        child_tax_percentage=0
                        for child_tax in tax_id.children_tax_ids:
                            child_tax_percentage=child_tax_percentage+child_tax.amount
                            if child_tax.tag_ids.name=='SGST':
                                self.sgst=self.quantity*self.price_unit*((child_tax.amount)/100)
                            elif child_tax.tag_ids.name=='CGST':
                                self.cgst=self.quantity*self.price_unit*((child_tax.amount)/100)
                            elif child_tax.tag_ids.name=='CESS':
                                if child_tax.amount_type=='percent':
                                    cess_amount=self.quantity*self.price_unit*((child_tax.amount)/100)
                                elif child_tax.amount_type=='fixed':
                                    cess_amount=self.quantity*self.price_unit+amount
                                self.cess=cess_amount
                        amount=self.quantity*self.price_unit*((child_tax_percentage)/100)
                    if tax_id.amount_type=='percent':
                        if tax_id.tag_ids.name=='IGST':
                            amount=self.quantity*self.price_unit*((tax_id.amount)/100)
                            self.igst=self.quantity*self.price_unit*((tax_id.amount)/100)
                    tax_amount=tax_amount+amount
                self.tax_amount=tax_amount
                self.price_total=self.quantity*self.price_unit+tax_amount


    @api.constrains('hsn')
    @api.multi
    def _check_hsn(self):
        if len(self.hsn)is not 8:
            raise Warning(_('Doc Date should not be less OR more than 8 digits...!'))


class EwayBillHistory(models.Model):
    _name = 'eway.bill.history'

    eway_bill_no=fields.Char(string='E-Way Bill No',track_visibility='onchange',)
    eway_bill_date=fields.Datetime(string='E-Way Bill Date',track_visibility='onchange',)
    valid_date=fields.Datetime(string='E-Way Bill Valid Upto',track_visibility='onchange',)
    eway_bill_history_id=fields.Many2one('eway.bill',string='E-Way History ID')

class VehicleHistory(models.Model):
    _name = 'eway.bill.vehicle.history'

    vehicle_no=fields.Char(string='Vehicle No',track_visibility='onchange',)
    vehicle_no_from=fields.Datetime(string='Vehicle Valid From',track_visibility='onchange',)
    vehicle_no_to=fields.Datetime(string='Vehicle Valid From Upto',track_visibility='onchange',)
    vehicle_no_history_id=fields.Many2one('eway.bill',string='E-Way History ID')