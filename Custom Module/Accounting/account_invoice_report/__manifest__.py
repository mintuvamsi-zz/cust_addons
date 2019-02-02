
{
    'name': 'Account Report',
    'version': '1.0',
    'category': 'Account Report',
    'sequence': 67,
    
    'description': "",
    'website': 'https://www.sailotech.com',
    'depends': ['account','base','l10n_in','mail',],
    'data': [
       
        'report/account_invoice.xml',
        'report/account_report.xml'
    ],
    'test': [
       
    ],
    'demo': [
        
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}