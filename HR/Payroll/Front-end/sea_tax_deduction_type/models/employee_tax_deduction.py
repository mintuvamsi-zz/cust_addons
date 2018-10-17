from odoo import api, fields, models, tools


class employeetaxdeduction(models.Model):
	_name = 'employee.taxdeduction.header'
	_rec_name='employee_id'
	
	employee_id =fields.Many2one('hr.employee',string="Employee ID")
	date = fields.Date(default=fields.Datetime.now(),string ='Date')
	employee_header_id=fields.One2many('employee.taxlines','employee_sectionlines',string='Employee History')

	
class employeetaxlines(models.Model):
	_name = 'employee.taxlines'
	# _rec_name='section_id'
	
	section_id = fields.Char(string='Section')
	deduction_desc = fields.Many2one('tds.taxdeductiontypes', string="Deduction Description")
	deduction_limit = fields.Integer(string='Deduction Limit')	
	amount = fields.Integer(string = 'Declared Amount')
	limit_level = fields.Selection([('S','Section'),('I','Individual'),('N','Non-Calculated')],  string='Limit Level')
	employee_sectionlines = fields.Many2one('employee.taxdeduction.header')
	allowed_limit = fields.Integer(string = 'Allowed Limit')
	factor = fields.Float(string = 'Factor(%)')



	@api.onchange('deduction_desc')
	def onchange_deduction_desc(self):
		if self.deduction_desc:
			self.section_id = self.deduction_desc.sectiontypes
			self.deduction_limit = self.deduction_desc.deduction_limit
			self.limit_level = self.deduction_desc.limit_level
			





	
	# @api.onchange('section_id')
	# def onchange_section_id(self):
	# 	if self.section_id:
	# 		self.deduction_desc = self.section_id.deduction_desc
	# 		self.deduction_limit = self.section_id.deduction_limit
