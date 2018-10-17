# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'HR Holidays Extended',
    'version': '1.2',
    'category': 'HR',
    'sequence': 61,

    'description': "",
    'website': 'https://www.sailotech.com',
    'depends': ['hr','base','l10n_in','web','mail','hr_holidays',],
    'data': [
	'security/hr_holidays_security.xml',
        'security/ir.model.access.csv',
		'data/mail_template_data.xml',


        'views/hr_compoff_view.xml',
        


    ],
    'test': [

    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
