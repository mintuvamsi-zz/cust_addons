from odoo import fields, models, tools, api

class PayslipMonthlyReportView(models.Model):

	_name = 'sea.payslip.monthly.report'
	_auto = False
	_order = 'period'


	id = fields.Integer(string = 'S.NO')
	emp_id = fields.Char(string = 'Employee ID')
	name = fields.Char(string = 'Employee Name')
	job_id = fields.Char(string = 'Job Title')
	department_id = fields.Char(string = 'Department')
	company_id = fields.Char(string = 'Company Name')
	state = fields.Selection([('draft', 'Draft'), ('verify', 'Waiting'), ('done', 'Done'), ('cancel', 'Rejected')],
                             string='Status')
	period = fields.Date(string = 'Period')
	date_to = fields.Date(string ='Date To')
	working_days = fields.Float(string = 'Working Days')
	basic = fields.Float(string = 'Basic')
	hra = fields.Float(string = 'HRA')
	spa_flexible = fields.Float(string = 'Special & Flexible Allowance')
	ntar = fields.Float(string = 'Non Taxable Reimbursment')
	project = fields.Float(string = 'Project')
	shift = fields.Float(string = 'Shift Allowance')
	incentives = fields.Float(string = 'Incentives')
	gross = fields.Float(string = 'Gross')
	gross_c = fields.Float(string = 'Gross For Contract')
	emp_pf = fields.Float(string = 'Employee PF')
	emp_esi = fields.Float(string = 'Employee ESI')
	pt = fields.Float(string = 'Professional Tax')
	medical_insurance = fields.Float(string = 'Medical Insurance')
	mv = fields.Float(string = 'Meal Vouchers')
	other_deductions = fields.Float(string = 'Other Deductions')
	unpaid_days = fields.Float(string = 'Unpaid Days')
	unpaid_days_cont = fields.Float(string = 'Unpaid Days for contract')
	tds = fields.Float(string = 'TDS')
	tdsc = fields.Float(string = 'Contract for TDS')
	total_deductions = fields.Float(string = 'Total Deductions')
	netsalary = fields.Float(string = 'Net Salary')
	netsalary_cont = fields.Float(string = 'Net Salary For Contract')


	@api.model_cr
	def init(self):
		# tools.drop_view_if_exists(self._cr, 'sea_payslip_monthly_report')
		self._cr.execute("select * from public.sea_payslip_monthly_report")




