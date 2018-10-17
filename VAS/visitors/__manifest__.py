# -*- coding: utf-8 -*-
{
    'name': "visitors",

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
    'category': 'visitors',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail','l10n_in'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
         'views/visitors_view.xml',
         #'views/visitor_config_setting.xml',
         'report/visitors.xml',
         'report/visitors_report.xml',
         #'report/new_wizard.xml',
         'report/visitors_report_month.xml',
         #'wizard/new_wiz_report.xml',         
         # 'wizard/report_visitors_bymonth.xml'
     ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}