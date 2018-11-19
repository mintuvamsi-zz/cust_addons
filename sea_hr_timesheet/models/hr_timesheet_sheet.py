# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
#     (www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _ 
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, AccessError
import pdb

class AccountAnalyticLine(models.Model):
    _name='account.analytic.line'

    _inherit= ['account.analytic.line','mail.thread']

    state=fields.Selection([('draft','Draft'),('confirm','Waiting Approval'),('done','Approved')
    ],string="State",default='draft',track_visibility='onchange')
    manager_status=fields.Boolean('Send To Manager', default=False)
    name = fields.Text('Description', required=True,track_visibility='onchange')

    # date_validation=fields.Boolean('Date Validation')
    # user_validation=fields.Boolean('User Validation')
    # time_validation=fields.Boolean('Time Validation')


  
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


    # @api.model
    # def create(self, values):
    #     # Override the original create function for the timesheet model
    #     pdb.set_trace()
    #     project_task=self.env['project.task'].search([('start_date', '>', values['date']),('date_to','<', values['date']),('estimated_hours','>','effectice_hours'),('user_id','=',self.env.uid)])
    #     if project_task:
    #         raise UserError(_("You can't apply timesheet for a project task which is expired or more then estimated hours"))
    #     return super(AccountAnalyticLine, self).create(vals)

    @api.onchange('date','task_id','project_id')
    def onchange_project_restriction(self):
        project_object=self.env['project.task']
        project_conf=self.env['res.config.settings']
        # pdb.set_trace()
        date_validation = self.env['ir.config_parameter'].sudo().get_param('sea_hr_timesheet.date_validation')
        user_validation = self.env['ir.config_parameter'].sudo().get_param('sea_hr_timesheet.user_validation')
        time_validation = self.env['ir.config_parameter'].sudo().get_param('sea_hr_timesheet.time_validation')
        task_list=[]

        if self.project_id.privacy_visibility == "followers":
            searched_list = project_object.search([('generic', '=', 'True')]).ids
            task_list.append(searched_list)
            # pdb.set_trace()

            if bool(date_validation)==True and bool(user_validation)==False:
                searched_list = project_object.search([('start_date', '>=', self.date), ('end_date', '<=', self.date)]).ids
                task_list.append(searched_list)
            elif bool(date_validation)==False and bool(user_validation)==True:
                searched_list = project_object.search([('user_id', '=', self.env.uid)]).ids
                task_list.append(searched_list)
            elif bool(date_validation)==True and bool(user_validation)==True:
                searched_list = project_object.search([('start_date', '>=', self.date), ('end_date', '<=', self.date),('user_id', '=', self.env.uid)]).ids
                task_list.append(searched_list)
            else:
                searched_list = project_object.search([]).ids
                task_list.append(set(searched_list))


            # if bool(time_validation) == True:
            #     pdb.set_trace()
            #     # if self.task_id.generic == False:
            #     if self.task_id:
            #         if (self.task_id.estimated_hours < (self.task_id.estimated_hours + self.unit_amount)):
            #             raise UserError(_("You cannot raise Timesheet, "
            #                           "\n If Actual hours are more than Estimated hours"))
            #             task_list.append(set(searched_list))

            flat_end = [val for sublist in task_list for val in sublist]
            return {'domain': {'task_id': [('id', 'in', flat_end)]}}

    @api.model
    def create(self, values):
        project_object = self.env['project.task']
        task_list = []

        time_validation = self.env['ir.config_parameter'].sudo().get_param('sea_hr_timesheet.time_validation')

        pdb.set_trace()
        if self.project_id.privacy_visibility == "followers":
            searched_list = project_object.search([('generic', '=', 'True')]).ids
            task_list.append(searched_list)

            if bool(time_validation) == True:
                if self.task_id:
                    # if values['task_id']== self.task_id:
                    if (self.task_id.estimated_hours < (self.task_id.effective_hours + self.unit_amount)):
                        raise UserError(_("You cannot raise Timesheet, "
                                              "\n If Actual hours are more than Estimated hours"))
                        record = super(AccountAnalyticLine, self).create(values)
                        return record