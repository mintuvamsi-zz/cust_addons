# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class visitorsreportbymonth(models.TransientModel):

    _name = 'visitors.report.month'
    #_inherit = "visitors.visitors"
    _description = 'Visitors By Month Report'
    # _rec_name='from_name'

    def _get_default_start_date(self):
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    def _get_default_end_date(self):
        date = fields.Date.from_string(fields.Date.today())
        return date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d')

    start_date = fields.Date(string='Start Date', required=True, default=_get_default_start_date)
    end_date = fields.Date(string='End Date', required=True, default=_get_default_end_date)
    
    # @api.one
    # @api.depends('email')
    # def _count_no_of_visitors(self):
    #     """Sets the amount support tickets owned by this customer"""
    #     self.no_of_visitors = self.email.search_count([('active', '=', True)])

    @api.multi
    def print_report(self):
        """
         To get the date and print the report
         @return: return report
        """
        self.ensure_one()
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        return self.env.ref('visitors.action_visitors_form_view').report_action(self, data=data)

    # def _print_report(self, data):
    #     return self.env._print_report('data')



# class visitorsreportbymonth(models.TransientModel):

# 	_name = 'visitors.report.month'
# 	_description = 'Visitors By Month Report'


#     def _get_default_category(self):
#         return self.env['hr.salary.rule.category'].search([('code', '=', 'NET')], limit=1)

#     def _get_default_start_date(self):
#         year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
#         return '{}-01-01'.format(year)

#     def _get_default_end_date(self):
#         date = fields.Date.from_string(fields.Date.today())
#         return date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d')

#     start_date = fields.Date(string='Start Date', required=True, default=_get_default_start_date)
#     end_date = fields.Date(string='End Date', required=True, default=_get_default_end_date)

    
#     @api.multi
#     def print_report(self):
#         """
#          To get the date and print the report
#          @return: return report
#         """
#         self.ensure_one()
#         data = {'ids': self.env.context.get('active_ids', [])}
#         res = self.read()
#         res = res and res[0] or {}
#         data.update({'form': res})
#         return self.env.ref('l10n_in_hr_payroll.action_report_hrsalarybymonth').report_action(self, data=data)


##############################################################################################################################################################
# class HrSalaryEmployeeBymonth(models.TransientModel):

#     _name = 'hr.salary.employee.month'
#     _description = 'Hr Salary Employee By Month Report'

#     def _get_default_category(self):
#         return self.env['hr.salary.rule.category'].search([('code', '=', 'NET')], limit=1)

#     def _get_default_start_date(self):
#         year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
#         return '{}-01-01'.format(year)

#     def _get_default_end_date(self):
#         date = fields.Date.from_string(fields.Date.today())
#         return date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d')

#     start_date = fields.Date(string='Start Date', required=True, default=_get_default_start_date)
#     end_date = fields.Date(string='End Date', required=True, default=_get_default_end_date)
#     employee_ids = fields.Many2many('hr.employee', 'payroll_year_rel', 'payroll_year_id', 'employee_id', string='Employees', required=True)
#     category_id = fields.Many2one('hr.salary.rule.category', string='Category', required=True, default=_get_default_category)

#     @api.multi
#     def print_report(self):
#         """
#          To get the date and print the report
#          @return: return report
#         """
#         self.ensure_one()
#         data = {'ids': self.env.context.get('active_ids', [])}
#         res = self.read()
#         res = res and res[0] or {}
#         data.update({'form': res})
#         return self.env.ref('l10n_in_hr_payroll.action_report_hrsalarybymonth').report_action(self, data=data)
