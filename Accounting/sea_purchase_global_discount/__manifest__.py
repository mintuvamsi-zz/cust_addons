# -*- coding: utf-8 -*-
{
    'name': "Purchase Discount",

    'summary': """ 
    ★As percentage
    Select 'Percentage' from Discount type and give discount percentage as Discount rate. System will update the value of Discount and Total

    ★ As amount
    Select 'Amount' from Discount type and give discount amount as Discount rate. System will update the value of Discount and Total""",

    'description': """ 
    ★As percentage
    Select 'Percentage' from Discount type and give discount percentage as Discount rate. System will update the value of Discount and Total

    ★ As amount
    Select 'Amount' from Discount type and give discount amount as Discount rate. System will update the value of Discount and Total""",

    'author': "Sailotech Pvt Ltd",
    'website': "http://www.Sailotech.com",
    'category': 'Purchase Discount',
    'version': '0.1',
    'depends': ['base','account','purchase'],
    'data': [

        'views/account_invoice_view.xml',
    ],

}