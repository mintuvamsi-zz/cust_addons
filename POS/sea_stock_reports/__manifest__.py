# -*- coding: utf-8 -*-
{
    'name': "Rack wise and Supplier Wise Stock Report's",

    'summary': """ Rack wise and Supplier Wise Stock Report's """,

    'description': """ Rack wise and Supplier Wise Stock Report's """,

    'author': "Sailotech Pvt Ltd",
    'website': "http://www.Sailotech.com",
    'category': 'Inventory and POS',
    'version': '0.1',
    'depends': ['base','stock','account','point_of_sale','product'],
    'data': [

        'security/ir.model.access.csv', 
        'views/stock_report_view.xml',
        'views/rackwise_report_view.xml',
        'views/marzin_view.xml',
        #'views/product_price_view.xml',
    ],

}