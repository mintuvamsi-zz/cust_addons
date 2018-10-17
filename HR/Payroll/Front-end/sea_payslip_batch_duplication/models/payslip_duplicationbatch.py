from odoo import api, fields, models, tools, _


class payslipbatchduplication(models.Model):
	
	_inherit = 'hr.payslip.run'
	_description = 'Payslip Batches'

	# batch_run_id = fields.One2many('hr.payslip.batch.wizard','paysliprun_id')

	

	# @api.multi
 #    def duplicate_batch(self):
 #    	in_runid=str(self.id)
 #        in_fromdt=str(self.date_start)
 #        in_todt=str(self.date_end)
 #        self._cr.execute( "select * from insert_same_data_with_batch('"+in_runid +"','"+in_fromdt+"','"in_todt+"')")
 #       # self._cr.fetchall()
	

	#name = fields.Many2one('hr.payslip.run', required=True, readonly=True, states={'draft': [('readonly', False)]})
	# date_start = fields.Date(string='Date From', required=True, readonly=True,
 #        states={'draft': [('readonly', False)]}, default=time.strftime('%Y-%m-01'))
	# date_end = fields.Date(string='Date To', required=True, readonly=True,
 #        states={'draft': [('readonly', False)]},
 #        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])