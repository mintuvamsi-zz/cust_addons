# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,timedelta,time
import pdb
import json
import base64
class ConsolidatedEwayBill(models.Model):
    """
    This model will create the Consolidated E-Way Bill
    """

    _name = "consolidated.eway.bill"
    _inherit = ['mail.thread']
    _description = "Create the Consolidated E-Way Bill"

    from_name = fields.Many2one('res.company', 'Company Name', default=lambda self: self.env['res.company']._company_default_get('eway.bill'))
    from_gstin=fields.Char(string='Company GSTIN',track_visibility='onchange',)
    from_place=fields.Char(string='From Place',track_visibility='onchange',)
    from_state=fields.Many2one('res.country.state','State Of Change', domain="[('country_id','=',104)]", store=True,track_visibility='onchange')
    vehicle_no=fields.Char(string='Vehicle No',track_visibility='onchange',)
    transport_mode=fields.Selection([('1','Road'),('2','Rail'),('3','Air'),('4','Ship'),],default='1',string = "Mode",track_visibility='onchange')
    transport_doc_no=fields.Char(string='Transporter Doc No',track_visibility='onchange',)
    transport_doc_date=fields.Date(string='Transporter Doc Date',track_visibility='onchange',default=datetime.now())
    consolidated_item_id=fields.One2many('consol.eway.bill.items','consol_eway_bill_id',string='Consolidated E-Way Bill Item',track_visibility='onchange')
    status=fields.Selection([('draft','Draft'),('active','Active'),('inactive','Inactive'),('cancel','Cancel'),],string = "Status",track_visibility='onchange',default='draft')
    eway_bill_no=fields.Char(string='E-Way Bill No',track_visibility='onchange',)
    eway_bill_date=fields.Datetime(string='Consolidated E-Way Bill Date',track_visibility='onchange',)
    # valid_date=fields.Datetime(string='E-Way Bill Valid Upto',track_visibility='onchange',)
   

    @api.multi
    @api.onchange('from_name') 
    def on_change_from_company_id(self):
      if self.from_name:
        # pdb.set_trace()
        self.from_gstin=self.from_name.vat


    @api.constrains('vehicle_no')
    @api.multi
    def _check_vehicle_no(self):
        if len(self.vehicle_no)>10:
            raise Warning(_('Improper Vehicle No, It should not be more than 10 digits...!'))

    @api.constrains('transport_doc_no')
    @api.multi
    def _check_transport_doc_no(self):
        if len(self.transport_doc_no)>15:
            raise Warning(_('Transporter Doc No should not be more than 15 digits...!'))




    @api.multi
    def consolidated_eway_bill(self):
        filename= 'consolidated_eway_bill.json'
        # # --------------------------------------------------------

        # context = dict(self._context or {})
        # active_ids = context.get('active_id', []) or []
        # eway_bill_no=self.env['eway.bill']
        # tokan_gen_time=eway_bill_no.browse(active_ids).tokan_gen_time

        # d1=datetime.strptime(tokan_gen_time, "%Y-%m-%d %H:%M:%S")
        # d1_ts = time.mktime(d1.timetuple())
        # d2=datetime.now()
        # print("Before if condition****************")
        # d2_ts = time.mktime(d2.timetuple())
        # if (int(d2_ts-d1_ts) / 60) >1:
        #     # pdb.set_trace()
        #     print("Inside if condition****************")
        #     self.auth()
        # # --------------------------------------------------------

        item_list=[]
        for bill_no in self.consolidated_item_id:
            res={}
            print("Inside for loop****************")
            res['ewbNo']=bill_no.eway_bill_no.eway_bill_no
            item_list.append(res)

        data={
           "version":"1.0.0123",
                "billLists":[{
                        "fromPlace":self.from_place,
                        "fromState":int(self.from_name.state_id.l10n_in_tin),
                        "vehicleNo":self.vehicle_no,
                        "transMode":self.transport_mode,
                        "TransDocNo":self.transport_doc_no,
                        "TransDocDate":self.transport_doc_date,
                        "tripSheetEwbBills": item_list
        },
        ]}

        print (type(data))
        print ("json data", data)

        d=json.dumps(data,indent=4)
        b = bytes(d, 'utf-8')
        export_id = self.env['excel.extended'].create({'excel_file': base64.encodestring(b), 'file_name': filename})

        return{
            'view_mode': 'form',
            'res_id': export_id.id,
            'res_model': 'excel.extended',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            # 'context': context,
            'target': 'new', }

class inventory_excel_extended(models.TransientModel):
    _name= "excel.extended"

    excel_file = fields.Binary('Dowload report Excel')
    file_name = fields.Char('Excel File', size=64)



class JsonOutput(models.TransientModel):
    _name = 'v.json.output'
    _description = 'JSON Report Output'

    name = fields.Char('File Name', size=256, readonly=True)
    filename = fields.Binary('File to Download', readonly=True)
    extension = fields.Char('Extension', default='JSON')

    @api.multi
    def download(self):
        self.ensure_one()
        # pdb.set_trace()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/document?model=%s&field=filename&id=%s&filename=%s.%s' % (self._name, self.id, self.name, self.extension),
            'target': 'self'
        }


class ConsolEwayBillItems(models.Model):
    _name = 'consol.eway.bill.items'


    eway_bill_no=fields.Many2one('eway.bill', string='E-Way Bill No',track_visibility='onchange')
    
    consol_eway_bill_id=fields.Many2one('consolidated.eway.bill',string='Consolidated E-Way bill ID')

