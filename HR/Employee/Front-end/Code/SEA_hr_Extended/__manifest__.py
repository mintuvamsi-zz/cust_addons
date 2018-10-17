# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SEA Employee Directory',
    'version': '1.1',
    'category': 'Human Resources',
    'sequence': 75,
    'summary': ' Extended Employees Details',
    'description': "",
    'website': 'https://www.sailotech.com',
    'images': [
        'images/hr_department.jpeg',
        'images/hr_employee.jpeg',
        'images/hr_job_position.jpeg',
        'static/src/img/default_image.png',
    ],
    'depends': [
        'base_setup',
        'mail',
        'resource',
        'web',
        'hr',
    ],
    'data': [
        
         'views/hr_views.xml',
        
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
