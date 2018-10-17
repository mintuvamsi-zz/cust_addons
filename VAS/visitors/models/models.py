# -*- coding: utf-8 -*-

from odoo import models, fields, api, time, tools, _
from odoo.exceptions import ValidationError
import uuid

from itertools import groupby
from datetime import datetime, timedelta, time
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT

from werkzeug.urls import url_encode

from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp

class visitors(models.Model):
    _name = 'visitors.visitors'
    _inherit = ['mail.thread']
    _rec_name='from_name'

    name = fields.Char('Badge Number', readonly=True)
    from_name = fields.Char(string='Name',required=True)
    mobile = fields.Char(string='Mobile', required=True)
    email = fields.Char(string='E-mail', required=True)
    coming_from = fields.Char(string='Coming From')
    visit_purpose = fields.Char(string='Visit Purpose')
    vistor_type = fields.Selection([('P','Permanent'),('C','Contract'),('V','Visitor')], track_visibility='always', string='Visitor Type')
    department_id = fields.Many2one('hr.job', string='Department', store=True)
    person_meet = fields.Many2one('hr.employee',string='Person To Meet')
    visited_date = fields.Date(string='Visited Date', default=fields.Datetime.now, readonly=True, store=True)
    time_from = fields.Datetime(string="Entry Time", default=fields.Datetime.now, readonly=True)
    time_to = fields.Datetime(string="Exit Time")
    status_id = fields.Selection([('I','IN'),('O','OUT')], string ='Status', track_visibility='always', required='always')
    id_card = fields.Char(string="ID Card Number")
    id_type = fields.Selection([('C','Company ID'),('G','Government Issued'),('O','Others')],default='C',string = "ID Card Type",track_visibility='always')
    personal_details = fields.Text()
    company_details = fields.Text()
    image = fields.Text()
    accessories_items = fields.Selection([('Y','Yes'),('N','No')], track_visibility='always',string='Accessories')
    collect_items = fields.Selection([('Y','Yes'),('N','No')], track_visibility='always', string="Collect Items", required=True)
    gender_type=fields.Selection([('M','Male'),('F','Female')], track_visibility='always', string="Gender")

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('visitors.visitors') or '/'
        vals['name'] = seq
        return super(visitors, self).create(vals)

    
    valid_from = fields.Datetime(string='Badge Valid From',  required=True)
    valid_to = fields.Datetime(string='Badge Valid To', required=True, )



######################################################################################################### 

# class visitorsreportbymonth(models.TransientModel):

#     _name = 'visitors.report.month'
#     _description = 'Visitors By Month Report'
#     # _rec_name='from_name'

#     def _get_default_start_date(self):
#         year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
#         return '{}-01-01'.format(year)

#     def _get_default_end_date(self):
#         date = fields.Date.from_string(fields.Date.today())
#         return date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d')

#     start_date = fields.Date(string='Start Date', required=True, default=_get_default_start_date)
#     end_date = fields.Date(string='End Date', required=True, default=_get_default_end_date)
    
#     @api.one
#     @api.depends('email')
#     def _count_no_of_visitors(self):
#         """Sets the amount support tickets owned by this customer"""
#         self.no_of_visitors = self.email.search_count([('active', '=', True)])
    # @api.multi
    # def print_report(self):
    #     """
    #      To get the date and print the report
    #      @return: return report
    #     """
    #     self.ensure_one()
    #     data = {'ids': self.env.context.get('active_ids', [])}
    #     res = self.read()
    #     res = res and res[0] or {}
    #     data.update({'form': res})
    #     return self.env.ref('l10n_in_hr_payroll.action_report_hrsalarybymonth').report_action(self, data=data)



########################################################################################################
    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100
#######################################################################################################
