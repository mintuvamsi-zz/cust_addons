from odoo import api, fields, models, tools, _

class PF_ECR_Reports(models.Model):
	_name = 'pf.ecr'
	_auto = False
	_description = "Professional Tax Reports"
	_order = 'date desc'

	id=fields.Integer()
	date=fields.Char(string='Month of year')
	uan=fields.Char(string='UAN Number')
	name=fields.Char(string='Member Name')
	gross_salary=fields.Integer(string='Gross Wages')
	basic_salary=fields.Integer(string='EPF Wages')
	eps=fields.Integer(string='EPS Wages')
	edli=fields.Integer(string='EDLI Wages')
	epf_contribution=fields.Integer(string='EPF Contribution remitted')
	eps_contribution=fields.Integer(string='EPS Contribution remitted')
	epf_eps_amount_diff=fields.Integer(string='EPF and EPS Diff remitted')
	ncp_days=fields.Integer(string='NCP Days')
	refund_of_advances=fields.Integer(string='Refund of Advances')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'pf_ecr')
		self._cr.execute("""
			CREATE VIEW pf_ecr AS 
					SELECT	a.id,
							to_char(a.date_from::timestamp with time zone, 'Mon-yyyy'::text) AS date,
							a.uan,
							a.name,
							a.amount AS gross_salary,
							b.wage AS basic_salary,
							b.eps,
							b.edli,
							round(b.wage * 12::numeric / 100::numeric, 0) AS epf_contribution,
							round(b.eps * 8.33 / 100::numeric, 0) AS eps_contribution,
							round(b.wage * 12::numeric / 100::numeric, 0) - round(b.eps * 8.33 / 100::numeric, 0) AS epf_eps_amount_diff,
							0 AS ncp_days,
							0 AS refund_of_advances
					FROM (SELECT hp.id,
							emp.uan,
							emp.name,
							hp.date_from,
							hpl.amount
					FROM 	hr_employee emp,
							hr_payslip hp,
							hr_payslip_line hpl,
							hr_contract hc
					WHERE hpl.code::text = 'GROSS'::text AND emp.id = hp.employee_id AND hpl.slip_id = hp.id AND hc.employee_id = emp.id
					GROUP BY emp.name, hp.date_from, hpl.amount, hp.id,emp.uan) a,
					(SELECT hp.id,
							emp.name,
							hp.date_from,
							hc.wage,

						CASE
						WHEN hc.wage > 15000::numeric THEN 15000::numeric
						ELSE hc.wage
						END AS eps,
						
						CASE
						WHEN hc.wage > 15000::numeric THEN 15000::numeric
						ELSE hc.wage
						END AS edli

					FROM 	hr_employee emp,
							hr_payslip hp,
							hr_payslip_line hpl,
							hr_contract hc
						WHERE hpl.code::text = 'BASIC'::text AND emp.id = hp.employee_id AND hpl.slip_id = hp.id AND hc.employee_id = emp.id
						GROUP BY emp.name, hp.date_from, hc.wage, hp.id) b
						WHERE a.name::text = b.name::text AND a.id = b.id AND a.uan IS NOT NULL
						GROUP BY a.name,a.uan, a.date_from, a.amount, b.wage, b.eps, b.edli, a.id, b.id
						ORDER BY a.date_from; 

						""")