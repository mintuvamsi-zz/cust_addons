# -*- coding: utf-8 -*-
{
    'name': "sea.accounts.hierarchy",

    # 'summary': """
    #     Short (1 phrase/line) summary of the module's purpose, used as
    #     subtitle on modules listing or apps.openerp.com""",

    # 'description': """
    #     Long description of module's purpose
    # """,

    'author': "sailotech",
    'website': "http://www.sailotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'accounting hierarchy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account_invoicing','hr', 'calendar', 'resource'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/coa.xml',
        'views/coa_test.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}