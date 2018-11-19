# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError
import pdb

class ManagerApproval(models.TransientModel):
    """
    This wizard will confirm the all the selected Draft Timesheets
    """

    _name = "manager.approval"
    _description = "Approve the Timesheets"

    @api.multi
    def manager_approve(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        if self.env.user.has_group('hr_timesheet.group_timesheet_manager'):
            for record in self.env['account.analytic.line'].browse(active_ids):
                if record.state == 'confirm':
                    record.state='done'
                    record.manager_status=False
        else:
            raise UserError(_("Only Managers Can Aprrove"))
        return {'type': 'ir.actions.act_window_close'}
