# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import math
from datetime import timedelta

from odoo import fields, models
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from datetime import datetime,timedelta,time
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons import decimal_precision as dp
from datetime import datetime
import qrcode
from odoo.exceptions import UserError, AccessError
import re
import time
from string import *
import pdb


HOURS_PER_DAY = 8


class CompOff(models.Model):
    _name = "hr.compoff"
    _inherit = ['mail.thread']
    _description = "Comp-Off"



    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    name = fields.Char('Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'To Approve'),
        ('validate', 'Approved'),
        ('refuse', 'Refused'),
        ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
            help="The status is set to 'To Submit', when a Comp-Off request is created." +
            "\nThe status is 'To Manager', when Comp-Off request is confirmed by user." +
            "\nThe status is 'Refused', when Comp-Off request is refused by manager." +
            "\nThe status is 'Approved', when Comp-Off request is approved by manager.")
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('category', 'By Employee Tag')
    ], string='Allocation Mode', readonly=True, required=True, default='employee',

        help='By Employee: Allocation/Request for individual Employee, By Employee Tag: Allocation/Request for group of employees in category')
    holiday_status_id = fields.Selection([('compoff', 'Comp-Off')], string="Leave Type", required=True, default="compoff")
    employee_id = fields.Many2one('hr.employee', string='Employee',required=True,index=True, readonly=True,default=_default_employee, track_visibility='onchange')
    number_of_days_temp = fields.Float('Allocation', copy=False, readonly=False,
        help='Number of days of the leave request according to your working schedule.')
    date_from = fields.Datetime('Start Date', required=True, index=True, copy=False, track_visibility='onchange')
    date_to = fields.Datetime('End Date', required=True, index=True, copy=False, track_visibility='onchange')
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department', readonly=True, store=True)
    # department_id = fields.Many2one(related='employee_id.department_id',relation='hr.department', string='Department',store=True)
    payslip_status = fields.Boolean('Reported in last payslips',
        help='Green this button when the leave has been taken into account in the payslip.')
    report_note = fields.Text('Employee Comments')
    notes = fields.Text('Reasons',)
    category_id = fields.Many2one('hr.employee.category', string='Employee Tag', readonly=True,
        help='Category of Employee')
    type = fields.Selection([
            ('remove', 'Leave Request'),
            ('add', 'Allocation Request')
        ], string='Request Type', required=True, readonly=True, index=True, track_visibility='always', default='add',

        help="Choose 'Leave Request' if someone wants to take an off-day. "
             "\nChoose 'Allocation Request' if you want to increase the number of leaves available for someone")
    can_reset = fields.Boolean('Can reset', compute='_compute_can_reset')
    meeting_id = fields.Many2one('calendar.event', string='Meeting')
    linked_request_ids = fields.One2many('hr.holidays', 'parent_id', string='Linked Requests')


    @api.multi
    def _compute_can_reset(self):
        """ User can reset a leave request if it is its own leave request
            or if he is an Hr Manager.
        """
        user = self.env.user
        group_hr_manager = self.env.ref('hr_holidays.group_hr_holidays_manager')
        for holiday in self:
            if group_hr_manager in user.groups_id or holiday.employee_id and holiday.employee_id.user_id == user:
                self.can_reset = True



    # @api.onchange('employee_id')
    # def _onchange_employee_id(self):
    #     if self.employee_id:
    #         self.department_id=self.employee_id.department_id

    @api.multi
    def action_draft(self):
        for holiday in self:
            if not holiday.can_reset:
                raise UserError(_('Only an HR Manager or the concerned employee can reset to draft.'))
            if holiday.state not in ['confirm', 'refuse']:
                raise UserError(_('Leave request state must be "Refused" or "To Approve" in order to reset to Draft.'))
            holiday.write({
                'state': 'draft',
                'first_approver_id': False,
                # 'second_approver_id': False,
            })
            linked_requests = holiday.mapped('linked_request_ids')
            for linked_request in linked_requests:
                linked_request.action_draft()
            linked_requests.unlink()
        return True


    @api.multi
    def action_confirm(self):
        if self.filtered(lambda holiday: holiday.state != 'draft'):
            raise UserError(_('Leave request must be in Draft state ("To Submit") in order to confirm it.'))
        template=self.env.ref('sea_compoff.employee_email_template_req')
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return self.write({'state': 'confirm'})

    @api.multi
    def _check_security_action_approve(self):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
            raise UserError(_('Only an HR Officer or Manager can approve leave requests.'))

    @api.multi
    def action_approve(self):
        # if double_validation: this method is the first approval approval
        # if not double_validation: this method calls action_validate() below
        self._check_security_action_approve()
        # pdb.set_trace()
        compoff=self.env['hr.holidays'].create({
                'employee_id':self.employee_id.id,
                'holiday_type':self.holiday_type,
                'category_id':self.category_id.id,
                'holiday_status_id':6,
                'name':self.name,
				'date_from':self.date_from,
				'date_to':self.date_to,
                'number_of_days_temp':self.number_of_days_temp,
                'department_id':self.department_id.id,
                'type':"add",
                'state':'confirm',
                })
        compoff.action_approve()
        template=self.env.ref('sea_compoff.employee_email_template_appr')
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return self.write({'state': 'validate'})

    @api.multi
    def action_refuse(self):
        # if double_validation: this method is the first approval approval
        # if not double_validation: this method calls action_validate() below
       
        # pdb.set_trace()
        if self.state=="validate":
            compoff=self.env['hr.holidays'].create({
                    'employee_id':self.employee_id.id,
                    'holiday_type':self.holiday_type,
                    'category_id':self.category_id.id,
                    'holiday_status_id':6,
                    'name':self.name+"Refused",
                    'date_from':self.date_from,
                    'date_to':self.date_to,
                    'number_of_days_temp':self.number_of_days_temp,
                    'department_id':self.department_id.id,
                    'type':"remove",
                    })
        template=self.env.ref('sea_compoff.employee_email_template_ref')
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return self.write({'state': 'refuse'})

        # self.state="validate"
        # current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        # for holiday in self:
        #     if holiday.state != 'confirm':
        #         raise UserError(_('Leave request must be confirmed ("To Approve") in order to approve it.'))

        #     # if holiday.double_validation:
        #     #     return holiday.write({'state': 'validate1', 'first_approver_id': current_employee})
        #     else:
        #         holiday.action_validate()


    # @api.onchange('employee_id')
    # def _onchange_employee_id(self):
    #     if self.employee_id:
    #         self.department_id=self.employee_id.department_id


    @api.multi
    def _remove_resource_leave(self):
        """ This method will create entry in resource calendar leave object at the time of holidays cancel/removed """
        return self.env['resource.calendar.leaves'].search([('holiday_id', 'in', self.ids)]).unlink()



    @api.multi
    def action_draft(self):
        for holiday in self:
            if not holiday.can_reset:
                raise UserError(_('Only an HR Manager or the concerned employee can reset to draft.'))
            if holiday.state not in ['confirm', 'refuse']:
                raise UserError(_('Leave request state must be "Refused" or "To Approve" in order to reset to Draft.'))
            holiday.write({
                'state': 'draft',
                'first_approver_id': False,
                'second_approver_id': False,
            })
            linked_requests = holiday.mapped('linked_request_ids')
            for linked_request in linked_requests:
                linked_request.action_draft()
            linked_requests.unlink()
        return True



    @api.multi
    def _check_security_action_refuse(self):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
            raise UserError(_('Only an HR Officer or Manager can refuse leave requests.'))

    @api.onchange('date_from')
    def _onchange_date_from(self):
        """ If there are no date set for date_to, automatically set one 8 hours later than
            the date_from. Also update the number_of_days.
        """
        date_from = self.date_from
        date_to = self.date_to

        # No date_to set so far: automatically compute one 8 hours later
        if date_from and not date_to:
            date_to_with_delta = fields.Datetime.from_string(date_from) + timedelta(hours=HOURS_PER_DAY)
            self.date_to = str(date_to_with_delta)

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            self.number_of_days_temp = self._get_number_of_days(date_from, date_to, self.employee_id.id)
        else:
            self.number_of_days_temp = 0

    @api.onchange('date_to')
    def _onchange_date_to(self):
        """ Update the number_of_days. """
        date_from = self.date_from
        date_to = self.date_to

        # Compute and update the number of days
        if (date_to and date_from) and (date_from <= date_to):
            self.number_of_days_temp = self._get_number_of_days(date_from, date_to, self.employee_id.id)
        else:
            self.number_of_days_temp = 0

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ Returns a float equals to the timedelta between two dates given as string."""
        from_dt = fields.Datetime.from_string(date_from)
        to_dt = fields.Datetime.from_string(date_to)

        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id)
            return employee.get_work_days_count(from_dt, to_dt)

        time_delta = to_dt - from_dt
        return math.ceil(time_delta.days + float(time_delta.seconds) / 86400)

    @api.multi
    def _check_security_action_validate(self):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
            raise UserError(_('Only an HR Officer or Manager can approve leave requests.'))

    @api.multi
    def action_validate(self):
        self._check_security_action_validate()

        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for holiday in self:
            if holiday.state not in ['confirm', 'validate1']:
                raise UserError(_('Leave request must be confirmed in order to approve it.'))
            if holiday.state == 'validate1' and not holiday.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                raise UserError(_('Only an HR Manager can apply the second approval on leave requests.'))

            holiday.write({'state': 'validate'})
            if holiday.double_validation:
                holiday.write({'second_approver_id': current_employee.id})
            else:
                holiday.write({'first_approver_id': current_employee.id})
            if holiday.holiday_type == 'employee' and holiday.type == 'remove':
                holiday._validate_leave_request()
            elif holiday.holiday_type == 'category':
                leaves = self.env['hr.holidays']
                for employee in holiday.category_id.employee_ids:
                    values = holiday._prepare_create_by_category(employee)
                    leaves += self.with_context(mail_notify_force_send=False).create(values)
                # TODO is it necessary to interleave the calls?
                leaves.action_approve()
                if leaves and leaves[0].double_validation:
                    leaves.action_validate()
        return True

    def _validate_leave_request(self):
        """ Validate leave requests (holiday_type='employee' and holiday.type='remove')
        by creating a calendar event and a resource leaves. """
        for holiday in self.filtered(lambda request: request.type == 'remove' and request.holiday_type == 'employee'):
            meeting_values = holiday._prepare_holidays_meeting_values()
            meeting = self.env['calendar.event'].with_context(no_mail_to_attendees=True).create(meeting_values)
            holiday.write({'meeting_id': meeting.id})
            holiday._create_resource_leave()

class SuperMangAppr(models.Model):

    _inherit ="hr.holidays"
    _description = "Leave"

    super_manager_approval_status=fields.Boolean('Description')
    more_than_three=fields.Boolean('More Than Three')
    approve=fields.Boolean('Approve')
    send_to_sup_mang=fields.Boolean("Sent to Super Manager", default=False)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('sent_super','Sent To Super Manager'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
        ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
            help="The status is set to 'To Submit', when a leave request is created." +
            "\nThe status is 'To Approve', when leave request is confirmed by user." +
            "\nThe status is 'Refused', when leave request is refused by manager." +
            "\nThe status is 'Approved', when leave request is approved by manager.")
    department_id = fields.Many2one(related='employee_id.department_id',relation='hr.department', string='Department',store=True)

    # @api.onchange('employee_id')
    # def change_department_id(self):
    #     # pdb.set_trace()
    #     if self.employee_id:
    #         if self.employee_id.department_id:
    #             self.department_id=self.employee_id.department_id

    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        # pdb.set_trace()

        if values['type']=='remove':
            account_analytic_line=self.env['account.analytic.line'].search([('date', '>=', values['date_from'][0:10]),('date','<=', values['date_to'][0:10]),('state','!=','draft'),('user_id','=',self.env.uid)])
            if account_analytic_line:
                raise UserError(_("You can't apply leave for a period for which you have already submitted your timesheet"))
        if values['number_of_days_temp']>3 and values['type']=='remove':
            values['more_than_three']=True
        record = super(SuperMangAppr, self).create(values)
        # pdb.set_trace()

        return record



    #--------Code for the leave changes after send to manager
    @api.multi
    def write(self,values):
        # pdb.set_trace()
        #if values['number_of_days_temp']
        if values.get('number_of_days_temp'):
            
            if values['number_of_days_temp']>3:
                values['more_than_three']=True

            elif values['number_of_days_temp']<4 :
                values['more_than_three']=False
        result=super(SuperMangAppr, self).write(values)
        return result
    #-------------------------------------------------------------


    @api.multi
    def submit_to_super_manager(self):
        # if self.number_of_days_temp>2:
        self.super_manager_approval_status=True
        self.more_than_three=False
        self.send_to_sup_mang=True
        self.state='sent_super'
        # pdb.set_trace()
        self.env['hr.super_manager'].sudo().create({
                'name': self.name,
                'state':self.state,
                'holiday_type':self.holiday_type,
                'holiday_status_id':self.holiday_status_id.id,
                'employee_id':self.employee_id.id,
                'number_of_days_temp':self.number_of_days_temp,

                'date_from': self.date_from,
                'holidays_id': self.id,
                'date_to': self.date_to,
                'department_id': self.department_id.id,
                'report_note': self.report_note,
            })
        template=self.env.ref('sea_compoff.employee_email_holidays_super_req')
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return True


    @api.multi
    def _check_security_action_approve(self):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
            raise UserError(_('Only an HR Officer or Manager can approve leave requests.'))


    @api.multi
    def _remove_resource_leave(self):
        """ This method will create entry in resource calendar leave object at the time of holidays cancel/removed """
        return self.env['resource.calendar.leaves'].search([('holiday_id', 'in', self.ids)]).unlink()



    @api.multi
    def action_approve(self):
        # if double_validation: this method is the first approval approval
        # if not double_validation: this method calls action_validate() below

        self._check_security_action_approve()
        # pdb.set_trace()
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for holiday in self:
            self.super_manager_approval_status=False
            if holiday.state != 'confirm':
                raise UserError(_('Leave request must be confirmed ("To Approve") in order to approve it.'))

            if holiday.double_validation:
                return holiday.write({'state': 'validate1', 'first_approver_id': current_employee.id})
            else:
                holiday.action_validate()
        # Code Change for avoiding comp off mail template##################
        if self.type=="remove" and self.holiday_status_id!=6:
            template=self.env.ref('sea_compoff.employee_email_holidays_appr')
            self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)

# -------------------New code added 20th Sept 2018-------------------
    @api.multi
    def action_validate(self):

        self._check_security_action_validate()

        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for holiday in self:
            if holiday.state not in ['confirm', 'validate1']:
                raise UserError(_('Leave request must be confirmed in order to approve it.'))
            if holiday.state == 'validate1' and not holiday.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                raise UserError(_('Only an HR Manager can apply the second approval on leave requests.'))

            holiday.write({'state': 'validate'})
            if holiday.double_validation:
                holiday.write({'second_approver_id': current_employee.id})
            else:
                holiday.write({'first_approver_id': current_employee.id})
            # if holiday.holiday_type == 'employee' and holiday.type == 'remove':
            #     holiday._validate_leave_request()
            if holiday.holiday_type == 'category':
                leaves = self.env['hr.holidays']
                for employee in holiday.category_id.employee_ids:
                    values = holiday._prepare_create_by_category(employee)
                    leaves += self.with_context(mail_notify_force_send=False).create(values)
                # TODO is it necessary to interleave the calls?
                leaves.action_approve()
                if leaves and leaves[0].double_validation:
                    leaves.action_validate()
        return True
# ----------------------------------------------------------------

    @api.multi
    def action_confirm(self):
        record = super(SuperMangAppr, self).action_confirm()
        # pdb.set_trace()
        # -----------------------New Code for timesheet generation
        if self.holiday_type == 'employee' and self.type == 'remove':
            self._validate_leave_request()
        # ---------------------------------------------------------
        self.super_manager_approval_status=False
        # -------------------------------------------------------------------
        """ Timesheet will be generated on leave validation only if a timesheet_project_id and a
            timesheet_task_id are set on the corresponding leave type. The generated timesheet will
            be attached to this project/task.
        """
        # create the timesheet on the vacation project
        # Code Change for avoiding comp off mail template
        if self['type']=='remove' and self['holiday_status_id']!=6:
            template=self.env.ref('sea_compoff.employee_email_holidays_req')
            self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return record

    @api.multi
    def action_draft(self):
        record=super(SuperMangAppr, self).action_draft()
        self.send_to_sup_mang=False
        # # -------------------Remove timesheet after Reset to Draft--------------
        
        timesheets = self.sudo().mapped('timesheet_ids')
        timesheets.write({'holiday_id': False})
        timesheets.unlink()
        self._remove_resource_leave()
        
        return record



    @api.multi
    def action_refuse(self):
        self._check_security_action_refuse()

        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for holiday in self:
            if holiday.state not in ['confirm', 'validate', 'validate1']:
                raise UserError(_('Leave request must be confirmed or validated in order to refuse it.'))

            if holiday.state == 'validate1':
                holiday.write({'state': 'refuse', 'first_approver_id': current_employee.id})
            else:   
                holiday.write({'state': 'refuse', 'second_approver_id': current_employee.id})
            # Delete the meeting
            if holiday.meeting_id:
                holiday.meeting_id.unlink()
            # If a category that created several holidays, cancel all related
            holiday.linked_request_ids.action_refuse()
        self._remove_resource_leave()
        self.write({'more_than_three': 'True','send_to_sup_mang':'False'})
        # # -------------------------------------------------------
        # # pdb.set_trace()
        timesheets = self.sudo().mapped('timesheet_ids')
        timesheets.write({'holiday_id': False})
        timesheets.unlink()
        # template=self.env.ref('sea_compoff.employee_email_holidays_refuse')
        # self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return True

    @api.multi
    def _check_security_action_refuse(self):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_user'):
            raise UserError(_('Only an HR Officer or Manager can refuse leave requests.'))



class SuperManaer(models.Model):
    _name = "hr.super_manager"
    _inherit = ['mail.thread']
    _description = "Super Maneger Approval"



    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)


    name = fields.Char('Description')
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('sent_super','Sent To Super Manager'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
        ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='confirm',
            help="The status is set to 'To Submit', when a leave request is created." +
            "\nThe status is 'To Approve', when leave request is confirmed by user." +
            "\nThe status is 'Refused', when leave request is refused by manager." +
            "\nThe status is 'Approved', when leave request is approved by manager.")
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('category', 'By Employee Tag')
    ], string='Allocation Mode', readonly=True, required=True, default='employee',

        help='By Employee: Allocation/Request for individual Employee, By Employee Tag: Allocation/Request for group of employees in category')
    holiday_status_id = fields.Many2one("hr.holidays.status", string="Leave Type", required=True, readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    employee_id = fields.Many2one('hr.employee', string='Employee',required=True,index=True, readonly=True,default=_default_employee, track_visibility='onchange')
    number_of_days_temp = fields.Float('Allocation', copy=False, readonly=False,
        help='Number of days of the leave request according to your working schedule.')
    date_from = fields.Datetime('Start Date', required=True, index=True, copy=False, track_visibility='onchange')
    date_to = fields.Datetime('End Date', required=True, index=True, copy=False, track_visibility='onchange')
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department', readonly=True, store=True)
    report_note = fields.Text('Employee Comments')
    notes = fields.Text('Reasons',)
    holidays_id=fields.Many2one('hr.holidays','Holidays ID')

    @api.multi
    def _remove_resource_leave(self):
        """ This method will create entry in resource calendar leave object at the time of holidays cancel/removed """
        # pdb.set_trace()
        return self.env['resource.calendar.leaves'].search([('holiday_id', 'in', self.ids)]).unlink()

    @api.multi
    def super_action_approve(self):
        self.state='validate'
        self.holidays_id.sudo().write({'state':'validate'})
        template=self.env.ref('sea_compoff.employee_email_holidays_super_appr')
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)

    @api.multi
    def super_action_refuse(self):
        self.state='refuse'
        self.holidays_id.sudo().write({'state':'refuse'})
        # # -------------------------------------------------------
        # pdb.set_trace()
        timesheets = self.holidays_id.sudo().mapped('timesheet_ids')
        timesheets.write({'holiday_id': False})
        timesheets.unlink()
        self.holidays_id._remove_resource_leave()

        template=self.env.ref('sea_compoff.employee_email_holidays_super_ref')
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)

    @api.multi
    def super_action_draft(self):
        self.state='draft'
        self.holidays_id.sudo().write({'state':'draft'})
        self.holidays_id.sudo().write({'more_than_three':True})
        self.holidays_id.sudo().write({'send_to_sup_mang':False})
        # # -------------------------------------------------------
        # pdb.set_trace()
        timesheets = self.holidays_id.sudo().mapped('timesheet_ids')
        timesheets.write({'holiday_id': False})
        timesheets.unlink()
        self.holidays_id._remove_resource_leave()


class Employee(models.Model):

    _inherit = "hr.employee"

    remaining_leaves = fields.Float(compute='_compute_remaining_leaves', string='Remaining Legal Leaves', inverse='_inverse_remaining_leaves',
        help='Total number of legal leaves allocated to this employee, change this value to create allocation/leave request. '
             'Total based on all the leave types without overriding limit.')
    current_leave_state = fields.Selection(compute='_compute_leave_status', string="Current Leave Status",
        selection=[
            ('draft', 'New'),
            ('confirm', 'Waiting Approval'),
            ('refuse', 'Refused'),
            ('sent_super','Sent To Super Manager'),
            ('validate1', 'Waiting Second Approval'),
            ('validate', 'Approved'),
            ('cancel', 'Cancelled')
        ])
    current_leave_id = fields.Many2one('hr.holidays.status', compute='_compute_leave_status', string="Current Leave Type")
    leave_date_from = fields.Date('From Date', compute='_compute_leave_status')
    leave_date_to = fields.Date('To Date', compute='_compute_leave_status')
    leaves_count = fields.Float('Number of Leaves', compute='_compute_leaves_count')
    show_leaves = fields.Boolean('Able to see Remaining Leaves', compute='_compute_show_leaves')
    is_absent_totay = fields.Boolean('Absent Today', compute='_compute_absent_employee', search='_search_absent_employee')

    def _get_remaining_leaves(self):
        """ Helper to compute the remaining leaves for the current employees
            :returns dict where the key is the employee id, and the value is the remain leaves
        """
        self._cr.execute("""
            SELECT
                sum(h.number_of_days) AS days,
                h.employee_id
            FROM
                hr_holidays h
                join hr_holidays_status s ON (s.id=h.holiday_status_id)
            WHERE
                h.state='validate' AND
                s.limit=False AND
                h.employee_id in %s
            GROUP BY h.employee_id""", (tuple(self.ids),))
        return dict((row['employee_id'], row['days']) for row in self._cr.dictfetchall())

    @api.multi
    def _compute_remaining_leaves(self):
        remaining = self._get_remaining_leaves()
        for employee in self:
            employee.remaining_leaves = remaining.get(employee.id, 0.0)

    @api.multi
    def _inverse_remaining_leaves(self):
        status_list = self.env['hr.holidays.status'].search([('limit', '=', False)])
        # Create leaves (adding remaining leaves) or raise (reducing remaining leaves)
        actual_remaining = self._get_remaining_leaves()
        for employee in self.filtered(lambda employee: employee.remaining_leaves):
            # check the status list. This is done here and not before the loop to avoid raising
            # exception on employee creation (since we are in a computed field).
            if len(status_list) != 1:
                raise UserError(_("The feature behind the field 'Remaining Legal Leaves' can only be used when there is only one "
                    "leave type with the option 'Allow to Override Limit' unchecked. (%s Found). "
                    "Otherwise, the update is ambiguous as we cannot decide on which leave type the update has to be done. "
                    "\n You may prefer to use the classic menus 'Leave Requests' and 'Allocation Requests' located in Leaves Application "
                    "to manage the leave days of the employees if the configuration does not allow to use this field.") % (len(status_list)))
            status = status_list[0] if status_list else None
            if not status:
                continue
            # if a status is found, then compute remaing leave for current employee
            difference = employee.remaining_leaves - actual_remaining.get(employee.id, 0)
            if difference > 0:
                leave = self.env['hr.holidays'].create({
                    'name': _('Allocation for %s') % employee.name,
                    'employee_id': employee.id,
                    'holiday_status_id': status.id,
                    'type': 'add',
                    'holiday_type': 'employee',
                    'number_of_days_temp': difference
                })
                leave.action_approve()
                if leave.double_validation:
                    leave.action_validate()
            elif difference < 0:
                raise UserError(_('You cannot reduce validated allocation requests'))

    @api.multi
    def _compute_leave_status(self):
        # Used SUPERUSER_ID to forcefully get status of other user's leave, to bypass record rule
        holidays = self.env['hr.holidays'].sudo().search([
            ('employee_id', 'in', self.ids),
            ('date_from', '<=', fields.Datetime.now()),
            ('date_to', '>=', fields.Datetime.now()),
            ('type', '=', 'remove'),
            ('state', 'not in', ('cancel', 'refuse'))
        ])
        leave_data = {}
        for holiday in holidays:
            leave_data[holiday.employee_id.id] = {}
            leave_data[holiday.employee_id.id]['leave_date_from'] = holiday.date_from
            leave_data[holiday.employee_id.id]['leave_date_to'] = holiday.date_to
            leave_data[holiday.employee_id.id]['current_leave_state'] = holiday.state
            leave_data[holiday.employee_id.id]['current_leave_id'] = holiday.holiday_status_id.id

        for employee in self:
            employee.leave_date_from = leave_data.get(employee.id, {}).get('leave_date_from')
            employee.leave_date_to = leave_data.get(employee.id, {}).get('leave_date_to')
            employee.current_leave_state = leave_data.get(employee.id, {}).get('current_leave_state')
            employee.current_leave_id = leave_data.get(employee.id, {}).get('current_leave_id')

    @api.multi
    def _compute_leaves_count(self):
        leaves = self.env['hr.holidays'].read_group([
            ('employee_id', 'in', self.ids),
            ('holiday_status_id.limit', '=', False),
            ('state', '=', 'validate')
        ], fields=['number_of_days', 'employee_id'], groupby=['employee_id'])
        mapping = dict([(leave['employee_id'][0], leave['number_of_days']) for leave in leaves])
        for employee in self:
            employee.leaves_count = mapping.get(employee.id)

    @api.multi
    def _compute_show_leaves(self):
        show_leaves = self.env['res.users'].has_group('hr_holidays.group_hr_holidays_user')
        for employee in self:
            if show_leaves or employee.user_id == self.env.user:
                employee.show_leaves = True
            else:
                employee.show_leaves = False

    @api.multi
    def _compute_absent_employee(self):
        today_date = datetime.datetime.utcnow().date()
        today_start = fields.Datetime.to_string(today_date)  # get the midnight of the current utc day
        today_end = fields.Datetime.to_string(today_date + relativedelta(hours=23, minutes=59, seconds=59))
        data = self.env['hr.holidays'].read_group([
            ('employee_id', 'in', self.ids),
            ('state', 'not in', ['cancel', 'refuse']),
            ('date_from', '<=', today_end),
            ('date_to', '>=', today_start),
            ('type', '=', 'remove')
        ], ['employee_id'], ['employee_id'])
        result = dict.fromkeys(self.ids, False)
        for item in data:
            if item['employee_id_count'] >= 1:
                result[item['employee_id'][0]] = True
        for employee in self:
            employee.is_absent_totay = result[employee.id]

    @api.multi
    def _search_absent_employee(self, operator, value):
        today_date = datetime.datetime.utcnow().date()
        today_start = fields.Datetime.to_string(today_date)  # get the midnight of the current utc day
        today_end = fields.Datetime.to_string(today_date + relativedelta(hours=23, minutes=59, seconds=59))
        holidays = self.env['hr.holidays'].sudo().search([
            ('employee_id', '!=', False),
            ('state', 'not in', ['cancel', 'refuse']),
            ('date_from', '<=', today_end),
            ('date_to', '>=', today_start),
            ('type', '=', 'remove')
        ])
        return [('id', 'in', holidays.mapped('employee_id').ids)]
