# -*- coding: utf-8 -*-
{
    'name': " Sailotech Project Extended",

    'summary': "Extension to Project's",

    'description': "Long description of module's purpose",

    'author': "Sailotech",
    'website': "http://www.sailotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','project','sea_project_modules'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/project_extended_view.xml',
        # 'views/project_extended_issue_view.xml',
        # 'views/project_extended_sprint_view.xml',
        'views/project_extended_task_view.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode

}
