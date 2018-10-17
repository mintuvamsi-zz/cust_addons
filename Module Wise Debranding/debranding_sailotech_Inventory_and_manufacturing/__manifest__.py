{
    'name': 'Debranding Sailotech Inventory & Manufacturing',
    'version': '1.1.0',
    'category': 'Sailotech Debranding Inventory and Manufacturing',
    
    'author': "sailotech Pvt Ltd",
    'description': "",
    'website': 'https://sailotech.com',
    'depends': ['stock','mrp'],
    'data': [

          'views/inventory_config_settings.xml',
          'views/run_schedulers.xml',
          'views/mrp_config_settings.xml'

    ],

    'installable': True,
    'auto_install': True,
    'application': True,
}