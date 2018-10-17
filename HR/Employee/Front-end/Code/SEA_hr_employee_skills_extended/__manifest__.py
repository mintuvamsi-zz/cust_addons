# -*- coding: utf-8 -*-
{
    'name': "Hr Employee Skills ",

    'summary': """
        Module to Maintain Employee Skills""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sailotech",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','project',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_documents_views.xml',
        'views/skill_view.xml',
    ],
    # only loaded in demonstration mode

}
