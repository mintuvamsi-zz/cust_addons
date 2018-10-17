{
	'name': 'Payslip Report',
	'version':'11.1.0',
	'description': """

	""",
	'author': 'SEA',
	'depends': ['base_setup','hr','mail','hr_payroll',],
	'data': [

		

		 'view/payslip_pdfreport.xml',
		 'view/hr_payslip_view.xml',
		 'print_report_payslip.xml',

		],
	'installable': True,
	'auto_install': False,
}
