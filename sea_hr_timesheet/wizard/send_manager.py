# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError
import pdb

class SendManager(models.TransientModel):
    """
    This wizard will confirm the all the selected Draft Timesheets
    """

    _name = "send.manager"
    _description = "Confirm the Timesheets to Send Manager"

    @api.multi
    def send_to_manager(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        for record in self.env['account.analytic.line'].browse(active_ids):
            #pdb.set_trace()
            if record.state == 'draft':
                record.state='confirm'
                record.manager_status=True
            # else:
            #     raise UserError(_("Selected timesheets cannot be processed as they are not in 'Waiting Approval' or 'Aprroved' state."))

        return {'type': 'ir.actions.act_window_close'}
