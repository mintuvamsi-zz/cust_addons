# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Inclusive Exclusive Taxes ",
    'version': '1.2',
    'category': "Accounts",
    'sequence': 60,
    
    'description': """
                        There are two important ways in which price of a good or service is denoted under a tax regime:
                        1.Price inclusive of taxes: It implies that the price of a good or service includes tax. The tax is not separately charged from the customer. Thus, Inclusive GST means that GST is included in the price of the product.
                        2.Price exclusive of taxes: This means that the price of good or service does not include tax. Tax is separately charged over and above the price of the product. The term ‘plus taxes’ is used in many cases.
                        """,

    'website': "https://www.sailotech.com",
    'depends': ['account','base','product'],
    'data': [

        'views/product_views.xml',

    ],

    # 'installable': True,
    # 'auto_install': False,
    # 'application': True,
}

