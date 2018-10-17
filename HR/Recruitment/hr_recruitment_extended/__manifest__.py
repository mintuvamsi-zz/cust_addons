{
	'name': 'Offer Letter and Recruitment',
	'version':'11.1.0',
	'description': """

	""",
	'author': 'Sailotech',
	'depends': ['base_setup','hr','mail','hr_recruitment','sailotech_job_requisition'],
	'data': ['wizard/hr_next_stages_view.xml',
			# 'wizard/application_stage_view.xml',
			'security/hr_recruitment_extended_security.xml',
			'security/ir.model.access.csv',
			
			'hr_applicant_view.xml',
			'data/mail_template_data.xml',
			

			],
	'installable': True,
	'auto_install': False,
}
