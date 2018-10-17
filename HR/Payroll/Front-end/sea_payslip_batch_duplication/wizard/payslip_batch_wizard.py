import time
from datetime import datetime, timedelta
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class hrpayslipbatchwizard(models.TransientModel):
	#_inherit = 'hr.payslip.run'

	_name = 'hr.payslip.batch.wizard'

	@api.model
	def _default_paysliprun(self):
		
		ticket_ids = self._context.get('active_ids', []) 
		#record = self.env['hr.payslip.run'].browse(ticket_ids[0] )
		return ticket_ids[0]

	paysliprun_id = fields.Many2one('hr.payslip.run', string='paysliprun id',default=_default_paysliprun)
	batch_from = fields.Many2one('hr.payslip.run','Batch Name')
	date_from = fields.Date(string='Date From')
	date_to = fields.Date(string='Date To')
	clear_existing_data = fields.Boolean('Clear Existing Data')
	
	
	@api.multi
	def duplicate_batch(self):
		p_tid=str(self.paysliprun_id.id)
		p_fid=str(self.batch_from.id)
		p_fromdt=str(self.date_from)
		p_todt=str(self.date_to)
		p_clrdata = str(self.clear_existing_data)
		self._cr.execute("select insert_same_data_with_batch_t1('"+p_tid+"','"+p_fid+"','"+p_fromdt+"','"+p_todt+"','"+p_clrdata+"')")
		self._cr.fetchall()