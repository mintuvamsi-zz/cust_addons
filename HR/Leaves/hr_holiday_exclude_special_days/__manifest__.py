# -*- coding: utf-8 -*-
# © 2017 Jérôme Guerriat
# © 2017 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'SEA(Leave - Exclude Public holidays)',
    'category': 'Human Resources',
    'summary': 'Gives the possibility to exclude weekends and public holidays from leave days',
    'website': 'https://www.sailotech.com/',
    'version': '11.0.1.0.0',
    'description': '''
Module modifying the HR leave:


- Public Holidays can be automatically excluded when the computation of leave days is done.

        ''',
    'author': 'Sailotech',
    'depends': [
        'hr_holidays',
    ],
    'data': [
        #'views/public_holiday.xml',
        # 'views/hr_holiday_views.xml',
        # 'wizards/generate_holiday_wizard.xml',
        #'security/ir.model.access.csv',
        #'data/public_holiday_data.xml',
    ],
    'images': [
        'static/description/hr_holiday_exclude_special_days_cover.png',
    ],
    'installable': True,
    'application': False,
}
