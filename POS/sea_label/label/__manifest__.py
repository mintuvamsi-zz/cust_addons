# See LICENSE file for full copyright and licensing details.
{
    'name': "label",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Sailotech",
    'website': "http://www.Sailotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'labels',
    'version': '1.0',
    'depends': ['base','product'],
    'data': [
        'data/report_paperformat.xml',
        'security/label.brand.csv',
        'security/label.config.csv',
        'security/ir.model.access.csv',
        'views/label_config_view.xml',
        'views/label_print_view.xml',
        'views/label_size_data.xml',
        'wizard/label_print_wizard_view.xml',
        'views/label_report.xml',
        'report/dynamic_label.xml',
        'views/address.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'images': ['static/description/Label.png'],
    'installable': True,
    'auto_install': False,
}
