
# -*- coding: utf-8 -*-
{
    'name': "taxdeductiontype",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sailotech",
    'website': "http://www.Sailotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'taxdeductiontype',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll','base','hr','l10n_in'],

    # always loaded
    'data': [        
        
        # 'views/tax_deduction_description_view.xml',
        'views/tds_taxdeduction_config_view.xml',
        'views/employee_tax_deduction_views.xml',
        'views/config_settings_payroll_views.xml',
        # 'security/ir.model.access.csv'
        # 'views/t.xml',

         
         
     ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}