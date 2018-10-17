# -*- coding: utf-8 -*-
{
    'name': "ideas",

    'summary': """
         A thought, a plan, 
         or suggestion about what to do. 
         an opinion or belief. 
         something that you imagine or picture in your mind.""",

    'description': """
        A thought or collection of thoughts that generate in the mind. An idea is usually generated with intent, but can also be created unintentionally. Ideas often form during brainstorming sessions or through discussions.
    """,

    'author': "sailotech",
    'website': "http://www.sailotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'iDeas',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','hr','l10n_in'],

    # always loaded
    'data': [
        'security/ideas_security.xml',
        'security/ir.model.access.csv',        
        'views/ideas_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}