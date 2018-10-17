# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
import time
import pdb
import requests

class Job_Requisition(models.Model):
    _name = "job.requisition"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    name=fields.Char("Name",track_visibility='onchange')
    job_id=fields.Many2one("hr.job","Job Position",track_visibility='onchange')
    start_date=fields.Date('Requisition Date',track_visibility='onchange')
    end_date=fields.Date('End Date',track_visibility='onchange')
    position_status = fields.Selection([('open','Open'),('hold','Hold'),('re-open','Re-Open'),('close','Close')],
                        string='Position Status',copy=False, 
                        index=True, track_visibility='onchange', default='open')
    num_positions=fields.Integer('No. Positions',track_visibility='onchange')
    description=fields.Text('Job Description',track_visibility='onchange')
    job_code = fields.Char('Job Code', track_visibility='onchange')
    designation = fields.Char('Designation', track_visibility='onchange')
    cost_center = fields.Char('Cost Center',track_visibility='onchange')
    employment_state = fields.Selection([('temporary','Temporary'),('permanent','Permanent')],
        string='Proposed Employment',copy=False, index=True, track_visibility='onchange', default='temporary')
    department_head=fields.Many2one("res.users","Department Head", track_visibility='onchange')
    reporting_head=fields.Many2one("res.users","Reporting Head", track_visibility='onchange')
    position_allocation = fields.Selection([('replacement','Replacement'),
                            ('addition_to_the_existing_resource','Addition to the existing Resource'),
                            ('new_position','New Position')],string='Position Allocation', 
                            copy=False, index=True, track_visibility='onchange', default='new_position')
    replacement_details = fields.Text('Replacement Details', track_visibility='onchange')
    qualification = fields.Many2one('hr.recruitment.degree', "Educational Qualification", track_visibility='onchange')
    desired_exp = fields.Char('Desired yrs of Exp',track_visibility='onchange')
    suggested_ctc = fields.Char('Suggested CTC',track_visibility='onchange')
    skills = fields.Text('Skills',track_visibility='onchange')
    place_of_work = fields.Selection([('onsite','Onsite'),('offsite','Offsite')], 
        string='Place of Work', copy=False, index=True, track_visibility='onchange', default='offsite')
    requested_by = fields.Many2one("res.users","Requested By",track_visibility='onchange')
    head_hr = fields.Many2one("res.users","Head HR",track_visibility='onchange')
    hr_date = fields.Date('Date',track_visibility='onchange')
    approved_by = fields.Many2one("res.users","Approved By",track_visibility='onchange')
    approval_date = fields.Date('Approval Date')
    state = fields.Selection([('draft', 'Draft'),('level1','Send to Tower Head'),('level2','Send to HR'),('level3','Send to MD'),('approved', 'Approved'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')


    @api.multi
    def approve_requisition(self):
        requisition_line_id=self.env['job.requisition.line']
        get_id=requisition_line_id.create({
        'name':self.name,
        'start_date':self.start_date,
        'end_date':self.end_date,
        'num_positions':self.num_positions,
        'description':self.description,
        'job_id':self.job_id.id,
        })
        if get_id:
            self.state='approved'
            old_recruitment=self.job_id.no_of_recruitment
            self.job_id.no_of_recruitment=old_recruitment+self.num_positions

            template = self.env.ref('sailotech_job_requisition.requisition_approval_email_template')
            self.env['mail.template'].browse(template.id).send_mail(self.id)
        return True


    @api.multi
    def button_send_to_pm(self):
        self.state='level1'

        template = self.env.ref('sailotech_job_requisition.requisition_request_approval_email_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id)
        return True


    @api.multi
    def button_send_to_hr(self):
        self.state='level2'

        template = self.env.ref('sailotech_job_requisition.requisition_request_approval_email_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id)
        return True

 
    @api.multi
    def button_send_to_md(self):
        self.state='level3'

        template = self.env.ref('sailotech_job_requisition.requisition_request_approval_email_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id)
        return True


class Job_Job(models.Model):
    _inherit="hr.job"

    requisition_id=fields.One2many('job.requisition.line','job_id','Requisition_line_id')
    recruitment_type = fields.Selection([('internal','Internal'),('external','External')],string="Recruitment Type")



class Job_Requisition_line(models.Model):
    _name = "job.requisition.line"

    name=fields.Char("Name")
    job_id=fields.Many2one("hr.job","Job Position")
    start_date=fields.Date('Start Date')
    end_date=fields.Date('End Date')
    num_positions=fields.Integer('No. Positions')
    description=fields.Text('Description')
    job_id=fields.Many2one('hr.job','Job ID')
