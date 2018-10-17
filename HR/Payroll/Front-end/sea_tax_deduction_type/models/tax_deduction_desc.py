
from odoo import api, fields, models, tools


class Hrpayrolltaxdeductiontype(models.Model):
	_name = 'tds.taxdeduction.description'
	_rec_name='deduction_desc'
	

	deduction_desc =fields.Many2one('tds.taxdeductiontypes', string="Deduction Description")
	employee_id =fields.Many2one('hr.employee',string="Employee ID")
	amount =fields.Integer()
	section_id = fields.Selection(
		[('A','Exemptions under section 10 & 17'),
		('B','Other income'),
		('C','Deductions under Chapter VI-A'),
		('D','Deductions under Chapter VI (sec 80C)')],
		string='Section')


	@api.onchange('deduction_desc')
	def onchange_deduction_desc(self):
		if self.deduction_desc:
			self.section_id = self.deduction_desc.sectiontypes