# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import psycopg2
import base64
import hashlib
import pytz
import threading

from email.utils import formataddr

from werkzeug import urls

from odoo.modules import get_module_resource
from datetime import datetime, timedelta, time
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class visitorspermonth(models.TransientModel):

    _name = 'visitors.per.month.summary'
    _inherit = 'visitors.visitors'
    _description = 'Visitors Per Month Summary Report'

    def _get_default_start_date(self):
        year = fields.Date.from_string(fields.Date.today()).strftime('%Y')
        return '{}-01-01'.format(year)

    def _get_default_end_date(self):
        date = fields.Date.from_string(fields.Date.today())
        return date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d')

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True, default=_get_default_end_date)

    #visited_date = fields.Date('visitors.visitors')

    # depts = fields.Many2many('visitors.visitors', 'summary_dept_rel', 'sum_id', 'dept_id', string='Department(s)')
    # holiday_type = fields.Selection([
    #     ('Approved', 'Approved'),
    #     ('Confirmed', 'Confirmed'),
    #     ('both', 'Both Approved and Confirmed')
    # ], string='Leave Type', required=True, default='Approved')

    # @api.multi
    # def print_report(self):
    #     self.ensure_one()
    #     [data] = self.read()
    #     if not data.get('depts'):
    #         raise UserError(_('You have to select at least one Department. And try again.'))
    #     departments = self.env['visitors.visitors'].browse(data['from_name'])
    #     datas = {
    #         'ids': [],
    #         'model': 'visitors.visitors',
    #         'form': data
    #     }
    #     return self.env.ref('visitors.visitors.action_report_visitorssummary').report_action(departments, data=datas)
    def print_report(self, data):
        return self.env.ref('visitors_visitors.action_report_visitorssummary').report_action(self, data=data)

    #month_by = fields.Datetime('Generate report')

        
    @api.multi
    def generate_report(self):
        p_id=str(self.id)
        self._cr.execute( "SELECT visited_date,COUNT(*) FROM visitors_visitors GROUP BY visited_date")
        # pdb.set_trace()
        self.tds_cal = self._cr.fetchone()[0]
        # self.env.cr.commit()

   

    