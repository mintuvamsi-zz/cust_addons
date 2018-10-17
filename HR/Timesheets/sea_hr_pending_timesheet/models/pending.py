from odoo import api, fields, models, _ 

class PendingTimeSheet(models.Model):
	_name= "pending.timesheet.rp"

	emp_id=fields.Char('Employee Id')
	employee=fields.Char('Employee')
	#day=fields.Text('Day',limit=12)
	day=fields.Date('Date')
	work_email=fields.Char('Work Email')
	manager_name=fields.Char('Manager')