{
    'name': 'Debranding Sailotech Purchase and Inventory',
    'version': '1.1.0',
    'category': 'Sailotech Debranding Purchase and Inventory',
    
    'author': "sailotech Pvt Ltd",
    'description': "Debranding Purchase and Inventory",
    'website': 'https://sailotech.com',
    'depends': ['purchase'],
    'data': [
          'views/purchase.xml',
          'views/purchas_econfig_settings.xml',
          'views/Inventory_config_settings.xml',
          'views/run_schedulers.xml',
 ],

    'installable': True,
    'auto_install': True,
    'application': True,
}