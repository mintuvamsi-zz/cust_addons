# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
import time
import pdb
import requests

class CancelEwayBill(models.TransientModel):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "cancel.eway.bill"
    _inherit = ['mail.thread']
    _description = "Cancel the E-Way bill using Government API"

    @api.multi
    def _default_gstin(self):
        context = dict(self._context or {})
        active_ids = context.get('active_id', []) or []
        eway_bill_no=self.env['eway.bill']
        gstin=eway_bill_no.browse(active_ids).gstin
        return gstin




    gstin=fields.Char('From GSTIN',default=_default_gstin,track_visibility='onchange')


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



    @api.multi
    def auth(self):
        # defining the api-endpoint
        API_ENDPOINT = "https://aspone.in/api/ewaybills/authenticate"
        # API_ENDPOINT = self.from_name.auth_url
        headers = {'content-type': 'application/json', 'accept': 'application/json','username': 'test_dlr222',
                'password':'test_dlr222',
                'gstin':self.gstin,
                'clientid':'snf3f9e69dfa0b76b12',
                'client-secret':'snfa6e36f63adad4db0'}
        
        r = requests.post(url = API_ENDPOINT,headers=headers)
        self.tokan_gen_time=datetime.now()

        auth_token = r.text
        print("The pastebin URL is:%s"%auth_token)



    @api.multi
    def cancel_eway_bill(self):

        context = dict(self._context or {})
        active_ids = context.get('active_id', []) or []
        eway_bill_no=self.env['eway.bill']
        tokan_gen_time=eway_bill_no.browse(active_ids).tokan_gen_time
        # pdb.set_trace()
        d1=datetime.strptime(str(tokan_gen_time), "%Y-%m-%d %H:%M:%S")
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
                   'gstin':self.gstin,
                   'clientid':'snf3f9e69dfa0b76b12',
                   'client-secret':'snfa6e36f63adad4db0'}
        # your source code here

        # data to be sent to api
        ewbno=eway_bill_no.browse(active_ids).eway_bill_no
        data = {
            "eway_bill":{
                "ewbNo": ewbno,
                "cancelRsnCode": 2,
                "cancelRmrk": "Cancelled the order"
                }
            }

        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT,headers=headers,data=json.dumps(data))
        # pdb.set_trace()
        # extracting response text
        pastebin_url = r.text
        print("The pastebin URL is:%s"%pastebin_url)





    # @api.multi
    # def _default_eway_bill_no(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     bill_no=eway_bill_no.browse(active_ids).eway_bill_no
    #     return bill_no

    # @api.multi
    # def _default_eway_bill_date(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     bill_date=eway_bill_no.browse(active_ids).eway_bill_date
    #     return bill_date

    # @api.multi
    # def _default_counter_party_name(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     name=eway_bill_no.browse(active_ids).to_name
    #     return name


    # @api.multi
    # def _default_counter_party_gstin(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     to_gstin=eway_bill_no.browse(active_ids).to_name
    #     return to_gstin

    # @api.multi
    # def _default_trans_type(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     trans_type=eway_bill_no.browse(active_ids).transaction_type
    #     return trans_type


    # @api.multi
    # def _default_doc_no(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     doc_no=eway_bill_no.browse(active_ids).doc_no
    #     return doc_no



    # @api.multi
    # def _default_doc_date(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     doc_date=eway_bill_no.browse(active_ids).doc_date
    #     return doc_date


    # @api.multi
    # def _default_counter_party_gstin(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     to_gstin=eway_bill_no.browse(active_ids).to_name.vat
    #     return to_gstin


    # @api.multi
    # def _default_price_total(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     amount=eway_bill_no.browse(active_ids).amount_total
    #     return amount

    # @api.multi
    # def _default_tax_amount(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_id', []) or []
    #     eway_bill_no=self.env['eway.bill']
    #     tax_amount=eway_bill_no.browse(active_ids).amount_tax
    #     return tax_amount




    # eway_bill_no=fields.Char(string='E-Way Bill No',track_visibility='onchange',default=_default_eway_bill_no)
    # eway_bill_date=fields.Date(string='E-Way Bill Date',track_visibility='onchange',default=_default_eway_bill_date)
    # counter_party_name=fields.Char(string='Counter Party Name',track_visibility='onchange',default=_default_counter_party_name)
    # counter_party_gstin=fields.Char(string='Counter Party GSTIN',track_visibility='onchange',default=_default_counter_party_gstin)
    # trans_type=fields.Char(string = "Trans Type",track_visibility='onchange',default=_default_trans_type)
    # doc_no=fields.Char(string='Document No',track_visibility='onchange',default=_default_doc_no)
    # doc_date=fields.Date(string='Document Date',track_visibility='onchange',default=_default_doc_date)
    # price_total = fields.Float(string='Toatal Amount', store=True,default=_default_price_total)
    # tax_amount=fields.Float(string="Tax Amount",default=_default_tax_amount)


    # @api.multi
    # def invoice_transffer(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', []) or []

    #     for record in self.env['account.invoice'].browse(active_ids):
    #         #pdb.set_trace()
    #         if record.invoice_status == 'Ready to Transfer':

    #             raise UserError(_("Selected invoice(s) cannot be confirmed to Transffered as they are not in 'Transffered' state."))
    #         record.invoice_status='Ready to Transfer'
    #     return {'type': 'ir.actions.act_window_close'}
