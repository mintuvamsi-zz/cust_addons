# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class PTReport(models.Model):
	_name = 'pt.report'
	_auto = False
	_description = "Professional Tax Reports"
	_order = 'date desc'

	id=fields.Integer(string='Id')
	monthly_salaries = fields.Char(string = 'Monthly Salaries')
	number_of_employee	   = fields.Integer(string='Number of Employee')
	rate_of_tax_per	   = fields.Integer(string='Rate of Tax per month')
	amount_of_tax_deduction  = fields.Integer(string='Amount of tax deduction')
	date    = fields.Char(string='Month of year')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'pt_report')
		self._cr.execute("""
			CREATE VIEW pt_report AS 
			 SELECT row_number() OVER () AS id,
					a.monthly_salaries,
					a.number_of_employee,
					a.rate_of_tax_per,
					a.amount_of_tax_deduction,
					a.date
						FROM (SELECT 'Up to 15000'::text AS monthly_salaries,
								count(hpl.employee_id)::integer AS number_of_employee,
								0 AS rate_of_tax_per,
								0 AS amount_of_tax_deduction,
								to_char(hrp.date_from::timestamp with time zone, 'Mon-YYYY'::text) AS date
							FROM hr_payslip_line hpl,
								hr_payslip hrp
							WHERE hpl.amount <= 15000::numeric AND hpl.slip_id = hrp.id AND hpl.code::text = 'BASIC'::text
								GROUP BY hrp.date_from
							UNION
							SELECT 'From 15001 to 20000'::text AS monthly_salaries,
								count(hpl.employee_id)::integer AS number_of_employee,
								150 AS rate_of_tax_per,
								(count(hpl.employee_id) * 150)::integer AS amount_of_tax_deduction,
								to_char(hrp.date_from::timestamp with time zone, 'Mon-YYYY'::text) AS date
							FROM hr_payslip_line hpl,
								hr_payslip hrp
							WHERE hpl.amount >= 15001::numeric AND hpl.amount <= 20000::numeric AND hpl.slip_id = hrp.id AND hpl.code::text = 'BASIC'::text
								GROUP BY hrp.date_from
							UNION
							SELECT 'Above 20001'::text AS monthly_salaries,
								count(hpl.employee_id)::integer AS number_of_employee,
								200 AS rate_of_tax_per,
								(count(hpl.employee_id) * 200)::integer AS amount_of_tax_deduction,
								to_char(hrp.date_from::timestamp with time zone, 'Mon-YYYY'::text) AS date
								FROM hr_payslip_line hpl,
								hr_payslip hrp
							WHERE hpl.amount >= 20001::numeric AND hpl.slip_id = hrp.id AND hpl.code::text = 'BASIC'::text
								GROUP BY hrp.date_from) a
								
								ORDER BY a.monthly_salaries;

								"""
									)