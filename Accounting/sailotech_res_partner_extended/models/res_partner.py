# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.

import base64
import datetime
import hashlib
import pytz
import threading
import re

from email.utils import formataddr

import requests
from lxml import etree
from werkzeug import urls

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
import pdb

class res_partner(models.Model):
   _inherit = 'res.partner'
 

   gst_export_name=fields.Selection([('Regular', 'Regular'),('Export', 'Export'),
      ('Deemed Export', 'Deemed Export'),('SEZ', 'SEZ'),], string='Customer Type',  
      default='Regular', required=True, track_visibility='onchange')
   vendor_type=fields.Selection([('Regular', 'Regular'),('Import', 'Import'),('Composite Dealer', 'Composite Dealer'),
      ('SEZ', 'SEZ'),], string='Vendor Type',  
      default='Regular', track_visibility='onchange')

   @api.onchange('country_id')
   def onchange_amount(self):
      if self.country_id:
         if self.country_id.id!=104:
            self.gst_export_name = 'Export'
            self.vendor_type='Import'

   @api.onchange('gst_export_name')
   def onchange_export_name(self):
      if self.vat:
         if self.gst_export_name=='Export':
            raise UserError(_("You entered GSTIN so you cant make this as an Export Type "))
   
   #constraint
   @api.constrains('zip')
   @api.one
   def _check_zip(self):
      zip_num = self.zip
      list_of_special=['^','~','+','&','@','(','[','!','#','$','%',']','*',')','$','/',',','.','-','_','=',':',';','"',"'"]
      alpha=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
      alpha_upper = [element.upper() for element in alpha]
      if zip_num:
         if len(str(zip_num)) > 6:
            raise Warning(_('ZIP code should not exced 6 digits...!'))
         if len(str(zip_num)) == 6:

            for char  in zip_num:
               if char in list_of_special:
                  raise Warning(_('ZIP code should not contain special characters...!'))
            for char  in zip_num:
               if char in alpha:
                  raise Warning(_('ZIP code should not contain Alphabets...!'))
               elif char in alpha_upper:
                  raise Warning(_('ZIP code should not contain Alphabets...!'))


   #constraint
   @api.constrains('vat')
   @api.one
   def _check_gstin(self):
      gstin_num = self.vat
      list_of_special=['^','~','+','&','@','(','[','!','#','$','%',']','*',')','$','/',',','.','-','_','=',':',';','"',"'"]
      alpha=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
      if gstin_num:
         if (len(str(gstin_num)) > 15):
            raise Warning(_('GSTIN should not be more than 15 characters...!'))

         if (len(str(gstin_num)) < 15):
               raise Warning(_('GSTIN No should not be less than 15 characters...!'))

         if len(str(gstin_num))==15:
            if (len(str(gstin_num)) == 15):
               for char  in gstin_num:
                  if char in list_of_special:
                     raise Warning(_('GSTIN No should not contain Special characters...!'))
               for char  in gstin_num:
                  if char in alpha:
                     raise Warning(_('GSTIN No should not contain Lowercase Alphabets...!'))





