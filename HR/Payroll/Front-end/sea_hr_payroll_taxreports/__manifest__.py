# -*- coding: utf-8 -*-
{
    'name': "HR PayRoll Tax Reports",

    'summary': """HR PayRoll Tax Reports Monthly wise
                    1.Professional Tax pdf and Pivot Reports
                    2.PF ECR .xlsx and Pivot Reports
                    3.ESI Return .xlsx and Pivot Reports """,

    'description': """HR PayRoll Tax Reports
                    1.Professional Tax pdf and Pivot Reports
                    2.PF ECR .xlsx and Pivot Reports
                    3.ESI Return .xlsx and Pivot Reports""",

    'author': "Sailotech Pvt Ltd",

    'website': "http://www.sailotech.com",

    'category': 'HR PayRoll Tax Reports',

    'version': 'SEA',
   
    'depends': ['base','hr_payroll','l10n_in_hr_payroll','report_xlsx','hr'],
   
    'data': [
    
          'views/pf_ecr_view.xml',
          'report/pf_esi_xl_view.xml',
          'wizard/esi_wizard_view.xml',
          #'wizard/image.xml',
          'views/esi_view.xml',
          'views/pt_view.xml',
          'report/pt_pdf.xml',
          'views/employee_view.xml',
          'wizard/pf_wizard_view.xml',

    
                                    ],

}