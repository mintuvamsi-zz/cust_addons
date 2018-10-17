# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#     (www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _ 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, AccessError
import pdb
class AccountAnalyticLine(models.Model):

    _inherit= "account.analytic.line"

    state=fields.Selection([('draft','Draft'),('confirm','Waiting Approval'),('done','Approved')
    ],string="State",default='draft')
    manager_status=fields.Boolean('Send To Manager', default=False)
    name = fields.Text('Description', required=True)

    # @api.model
    # def create(self, values):
    #     account_analytic_line=self.env['account.analytic.line'].search([('date', '=', values['date'])])
    #     entered_hours=0
    #     for line in account_analytic_line:
    #         entered_hours=entered_hours+line.unit_amount
        
    #     entered_hours=entered_hours+values['unit_amount']
    #     if entered_hours>24:
    #         raise UserError(_('Working hours should not be more than 24 hours in a day'))
    #     record = super(AccountAnalyticLine, self).create(values)
    #     return record

   

    @api.multi
    def send_to_manager(self):
        self.state='confirm'
        self.manager_status=True

    @api.multi
    def approval(self):
        self.state='done'
        # pdb.set_trace()
        self.manager_status=False

    @api.multi
    def refuse(self):
        self.state='draft'
        self.manager_status=False
