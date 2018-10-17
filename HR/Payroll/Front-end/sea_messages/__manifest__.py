# -*- coding: utf-8 -*-
{
    'name': "SEA MESSAGES MASTER",

    'summary': """
             SEA PAYROLL MESSAGES""",

    'description': """
       sea payroll messages
       
    """,

    'author': "Sailotech Pvt Ltd",
    'website': "http://www.Sailotech.com",
    'category': 'sea payroll message Details',
    'version': '11',
    'depends': ['hr_contract','l10n_in_hr_payroll',],
    'data': [
        'views/messages_views.xml',
        'views/master_messages.xml',
        'views/log_messages.xml',
        'views/log_error.xml',
        'security/ir.model.access.csv',
    ],

}