{
    'name': 'Debranding Sailotech POS',
    'version': '1.1.0',
    'category': 'Sailotech POS Debranding',
    
    'author': "Sailotech Pvt Ltd",
    'description': "SEA POS Debranding",
    'website': 'https://sailotech.com',
    'depends': ['point_of_sale'],

    'data': [ 'views/pos.xml','views/pos_config_view.xml', ],

    'qweb': ['static/src/xml/pos.xml'],

    'installable': True,
    'auto_install': True,
    'application': True,
}