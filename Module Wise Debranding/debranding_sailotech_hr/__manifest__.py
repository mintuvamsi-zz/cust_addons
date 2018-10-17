{
    'name': 'Debranding Sailotech HR',
    'version': '1.1.0',
    'category': 'Debranding',
    
    'author': "sailotech Pvt Ltd",
    'description': "",
    'website': 'https://sailotech.com',
    'depends': ['hr_payroll','l10n_in_hr_payroll','hr_timesheet','project'],
    'data': [
          'views/payroll_config_settings.xml',
          'views/timesheet_config_settings.xml',
          'views/project_config_settings.xml',

    ],

    'installable': True,
    'auto_install': True,
    'application': True,
}