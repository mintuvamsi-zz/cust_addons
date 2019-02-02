# -*- coding: utf-8 -*-

#
##############################################################################
{
    'name': 'SEA Payroll-Payslip Reporting',
    'version': '11.0.1.0.0',
    'summary': """SEA Payslip Pivot View Report.""",
    'description': """ SEA Payslip monthly report.
    This module gives a pivot view for the HR managers. they can see all the 'NET' amount of payslips in all states""",
    'author': 'Sailotech Pvt Ltd',
    'company': 'Sailotech Pvt Ltd',
    'maintainer': 'Sailotech Pvt Ltd',
    'website': 'https://www.sailotech.com',
    'category': 'Generic Modules/Human Resources',
    'depends': ['hr_payroll'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        # 'views/menu_payslip_report.xml'
        'views/payslip_monthly_report_menu.xml'
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
}
