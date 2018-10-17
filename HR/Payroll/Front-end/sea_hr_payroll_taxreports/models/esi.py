from odoo import api, fields, models, tools, _

class ESI_Reports(models.Model):
	_name = 'esi.rtrn'
	_auto = False
	_description = "Employees State Insurance"
	_order = 'date desc'
	_rec_name = 'ip_name'

	id=fields.Char()
	ip_number=fields.Char(string= 'IP Number')
	ip_name=fields.Char(string='IP Name')
	no_of_days=fields.Char(string='No of Days')
	wage=fields.Char(string='Total Monthly Wages')
	employees_contribution=fields.Char(string='Employees Contribution')
	employers_contribution=fields.Char(string='Employers Contribution')
	reason_code=fields.Char(string='Reason Code')
	last_working_day=fields.Char(string='Last Working Day')
	date=fields.Char(string='Month of year')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'esi_rtrn')
		self._cr.execute("""
			CREATE VIEW esi_rtrn AS  
				SELECT hpl.id,
					emp.ip_number,
					emp.name AS ip_name,
					0 AS no_of_days,
					hpl.amount AS wage,
					round(hpl.amount * 1.75/100) as employees_contribution,
					round(hpl.amount * 4.75/100) as employers_contribution,
					hrc.code AS reason_code,
					emp.last_day AS last_working_day,
					to_char(hrp.date_from::timestamp with time zone, 'Mon-YYYY'::text) AS date
				FROM hr_payslip_line hpl,
					hr_employee emp,
					hr_payslip hrp,
					hr_code hrc
				WHERE hpl.code::text = 'GROSS'::text AND hpl.employee_id = emp.id AND hpl.slip_id = hrp.id 
				AND hrc.id = emp.reason_code AND hpl.amount <=21000;


								"""
									)