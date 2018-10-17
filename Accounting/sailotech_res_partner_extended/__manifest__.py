# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.

{
    'name': 'Res Partner Extended',
    'version': '1.2',
    'category': 'Accounts',
    'sequence': 60,
    
    'description': "This module is the extended version of the res.partner module",
    'website': 'https://www.sailotech.com',
    'depends': ['account','base','l10n_in'],
    'data': [
       
        'views/res_company_view.xml',
        'views/res_partner_views.xml',
        'views/res_country_view.xml',
      
       
       
    ],
    'test': [
       
    ],
    'demo': [
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
