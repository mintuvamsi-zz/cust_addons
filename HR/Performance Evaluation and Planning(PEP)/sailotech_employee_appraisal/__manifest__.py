# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Appraisal',
    'version': '11.0.1',
    'category': 'Human Resources',
    'sequence': 75,
    'summary': 'Jobs, Departments, Employees Details',
    'description': """
Human Resources Management
==========================

This application enables you to manage important aspects of your company's staff and other details such as their skills, contacts, working time...


You can manage:
---------------
* Employees and hierarchies : You can define your employee with User and display hierarchies
* HR Departments
* HR Jobs
    """,
    'website': 'https://www.odoo.com/page/employees',
    'images': [

    ],
    'depends': [
        'base_setup',
        'mail',
        'hr',
        'SEA_hr_Extended',



    ],
    'data': [
        'security/ir.model.access.csv',
         'default_data.xml',
         #'employee_grade_view.xml',
         'periodic_appraisal_view.xml',
        
         #'appraisal_cron_view.xml',
         'data/mail_template_data.xml',
         

    ],
    'demo': [],
    'test': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
