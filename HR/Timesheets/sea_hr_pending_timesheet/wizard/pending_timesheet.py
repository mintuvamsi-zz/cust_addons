from odoo import api, fields, models, _

class Pending(models.TransientModel):
	_name = "pending.between"
	_description = "Pending Timesheets"

	start_date = fields.Date('From Date', default=fields.Datetime.now(), required=True)
	end_date = fields.Date('To Date', default=fields.Datetime.now(), required=True)

	def pending_timesheets(self):
		p_date_from=self.start_date
		p_date_to=self.end_date

		self._cr.execute("SELECT * FROM pending_timesheet_v('"+p_date_from+"', '"+p_date_to+"')")
		tree_view_id = self.env.ref('sea_hr_pending_timesheet.pending_timesheet_tree').id
		return{ 'type': 'ir.actions.act_window',
		 'views': [(tree_view_id, 'tree')],
		 'view_mode': 'tree',
		 'name': _('Pending Timesheets'),
		 'res_model': 'pending.timesheet.rp',
		 'target':'current',
		 'context': self.env.context,
		 }
