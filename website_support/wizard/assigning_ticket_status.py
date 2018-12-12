# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import api, fields, models
from openerp import tools
from random import randint
import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import logging
import pdb
_logger = logging.getLogger(__name__)
from odoo import SUPERUSER_ID


################################################################################################

class assigning_ticket_status(models.TransientModel):
    _name = "assigning.ticket.status"
    
    user_id = fields.Many2one('res.users', string="Assigned User")
    assigned_time = fields.Datetime(string="Assigned Time")
    closed_time = fields.Datetime(string="Closed Time")
    


    def update_status(self):
        # pdb.set_trace()
        """ Update the Ticket status in the Help Desk """
        ticket_obj = self.env['website.support.ticket']

        ticket_status_obj = self.env['assigned.ticket.history.lines']
        #wizard = self.browse(cr, uid, ids[0], context)
        ticket_ids = self._context.get('active_ids', [])
        user_id = []
        ticket_class = ticket_obj.browse(ticket_ids)
        for obj in ticket_class.assigned_line_item:
            if obj.user_id:
                user_id.append(obj.user_id)
        if self.user_id not in user_id:
            # Gets the status of the Ticket
            #pdb.set_trace()
            ticket_id = ticket_status_obj.create({
                'website_id' : ticket_ids[0],
                'user_id' : self.user_id.id,
                'assigned_time' : self.assigned_time,
                'closed_time' : self.closed_time,
                })
        ticket_class.write({'user_id':self.user_id.id})
        #ticket_ids.write(ticket_ids, {'user_id':self.user_id})
        # ticket_class.write({'user_id':self.user_id})


     
assigning_ticket_status()
