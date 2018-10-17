
{
    'name': "Debranding Sailotech",

    'summary': """
        Sailotech - One of the top ERP software solution provider company.""",

    'description': """
        Sailotech - One of the top ERP software solution provider company.
    """,

    'author': "Sailotech",
    'website': "www.sailotech.com",
    'category': 'Debranding',
    'version': '11.0.1.0.1',
    'depends': ['web','base_setup','web_settings_dashboard','web_planner', 'base', 'website', 'im_livechat', 'mail',
                 'web_responsive', 'backend_theme_v11' ],
    'data': [
        'views/views.xml',
        'views/website_config_settings.xml',
        'views/res_config_settings.xml',
        'views/partner.xml',
        'views/company_report.xml',
        'views/dbs.xml',
        'views/stylesheet.xml',
        'views/app_hide_view.xml',
        'views/assets.xml',
        'views/app_hide_view.xml',
        'views/webclient_templates.xml',
        'views/edit_company_view.xml'

    ],


    'qweb':[
            'static/src/xml/base.xml',
            'static/src/xml/dashboard.xml',
            'static/src/xml/client_action.xml',

    ],
    
    'installable': True,
    'auto_install': True,
    'application': True,
}
