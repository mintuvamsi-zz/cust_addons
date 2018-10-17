{
	'name': 'Sailotech Job Requisition',
	'version':'11.1.0',
	'description': """

	""",
	'author': 'Sailotech Pvt Ltd',
	'depends': ['base_setup','hr','mail','hr_recruitment'],
	'data': [
		#'wizard/hr_next_stages_view.xml',
		'security/ir.model.access.csv',

		'job_requisition_view.xml',
		'data/mail_template_data.xml',

			],
	'installable': True,
	'auto_install': False,
}
