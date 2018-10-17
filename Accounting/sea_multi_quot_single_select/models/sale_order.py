# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.

import base64
import hashlib
import pytz
import threading

from email.utils import formataddr

from werkzeug import urls

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
import pdb

class sale_order_line(models.Model):
	_inherit ="sale.order.line"
	selected = fields.Boolean(string='Select', default=False)


class sale_order(models.Model):
	_inherit="sale.order"

	@api.multi
	def action_confirm(self):
		pdb.set_trace()
		super(sale_order, self).action_confirm()
		if not len(self.order_line)==1 and len(self.order_line)>1:
			print("################ INSIDE ACTION QUOTAION SEND #################")
			cr = self.env.cr
			cr.execute("update sale_order_line set product_uom_qty=0, qty_delivered=0, qty_invoiced=0, price_unit=0, price_subtotal=0 where selected='f' and order_id="+str(self.id))
			for record in self.order_line:
				if record.selected==False:
					record.tax_id=0
		# self.ensure_one()
      	# context = self._context
     	# # Validation is skipped for brevity
    	# selection = context['product_id']
    	# # do things with selection data
 