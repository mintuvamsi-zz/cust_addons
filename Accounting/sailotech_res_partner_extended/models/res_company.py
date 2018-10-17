# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    
    ecom_gst_id=fields.One2many('ecom.gst','company_id','Ecom GST ID')
    

class EcomGstin(models.Model):
    _name='ecom.gst'

    name=fields.Char('Name')
    ecom_gstin=fields.Text('Ecom GST')
    company_id=fields.Many2one('res.company','Company')






