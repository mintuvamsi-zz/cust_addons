# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sailotech Jewellery',
    'version': '1.2',
    'category': 'Product',
    'sequence': 60,
    
    'description': "",
    'website': 'https://www.odoo.com/page/purchase',
    'depends': ['account','base','l10n_in','sale','product','bi_professional_reports_templates',],
    'data': [
          'wizard/product_wizard_view.xml',
          'views/product_view.xml',
          'views/product_product_view.xml',
          'views/account_invoice_view.xml',
          'views/res_company_view.xml',
          'views/account_report.xml',
          
          
        # 'wizard/account_invoice_refund_view.xml',
        # 'views/account_invoice_views.xml',
        # 'views/res_company_view.xml',
          'views/sale_view.xml',
          'views/daily_price_view.xml'
        # 'views/transactions_view.xml',
       # 'views/res_partner_views.xml',
        
        #'views/xattax_config_settings_views.xml',
        # 'report/invoice_report.xml',
        # 'report/invoice_template.xml',
        #'security/ir.model.access.csv',
        
       
    ],
    'test': [
       
    ],
    'demo': [
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}