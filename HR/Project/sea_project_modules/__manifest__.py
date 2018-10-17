# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.
{
    'name': "sailotech_project_modules",

    'summary': "Extension to Project's. Contains Modules & Submodules",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sailotech pvt. ltd.",
    'website': "http://www.sailotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base','project',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/modules_views.xml',
        'views/submodule_view.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    
}