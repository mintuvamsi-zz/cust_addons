# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ReportHelpDesk(models.Model):
    _name = "report.helpdesk"

    support_ticket_id = fields.Many2one('website.support.ticket', string="Support Ticket")
    person_name = fields.Char(related="support_ticket_id.person_name", string="Customer Name")
    ticket_number_display = fields.Char(related="support_ticket_id.ticket_number_display", string="Ticket Number")
    state = fields.Many2one('website.support.ticket.states', readonly=True, related="support_ticket_id.state", string="State")
    open_time = fields.Datetime(related="support_ticket_id.create_date", string="Open Time")    
    close_time = fields.Datetime(related="support_ticket_id.close_time", string="Close Time")
    total_hours = fields.Float(string="Total")
    # effective_hours = fields.Float(string='Hours Spent', related="task_id.effective_hours", help="Computed using the sum of the task work done.")

    # def _select(self):
    #     return super(ReportProjectTaskUser, self)._select() + """,
    #         progress as progress,
    #         t.effective_hours as hours_effective,
    #         remaining_hours as remaining_hours,
    #         total_hours as total_hours,
    #         t.delay_hours as hours_delay,
    #         planned_hours as hours_planned"""

    def _group_by(self):
        return super(ReportProjectTaskUser, self)._group_by() + """,
            total_hours"""
