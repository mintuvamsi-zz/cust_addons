# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Order Extended',
    'version': '1.0',
    'category': 'Sale and Purchase',
    'sequence': 66,
    
    'description': "",
    'website': 'https://www.sailotech.com',
    'depends': ['account','base','l10n_in','sale'],
    'data': [
       
        # 'views/res_company_view.xml',
        'views/sale_order_views.xml',
      
       
       
    ],
    'test': [
       
    ],
    'demo': [
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
