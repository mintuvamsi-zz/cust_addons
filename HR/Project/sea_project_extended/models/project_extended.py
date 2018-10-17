# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, date
from lxml import etree
import time

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from odoo.tools.safe_eval import safe_eval
import pdb

class project_extended(models.Model):
    _inherit = "project.project"
    _description = 'Project'
    _order = 'sequence, id'


    project_new_id = fields.Char('Project Id', )
    description = fields.Text('Description')
   # alias_model=fields.Char("Alias Model")
    state=fields.Char("State")
    # pdb.set_trace()
    


class project_extended_task(models.Model):
    _inherit = "project.task"
    _description = 'Task'

    
    requirement_id=fields.Char('Requirement Id' , track_visibility='onchange')
    requirement_name=fields.Char('Requirement Name', track_visibility='onchange')
    module_id=fields.Many2one('project.modules','Module', track_visibility='onchange')
    submodule_id=fields.Many2one('project.modules.line','Sub Module', track_visibility='onchange')
    #'tech': fields.char('Tech')
    dev_type=fields.Selection([('tech','Tech'),('non-tech','Non-Tech'),('testing','Testing')],'Development Type', track_visibility='onchange')
    technical=fields.Selection([('java','Java'),('database','Database')],'Technical', track_visibility='onchange')
    estimated_hours=fields.Integer('Estimated Hours', track_visibility='onchange')
    # actual_hours=fields.Integer('Actual Hours')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Moderate'),
        ('2', 'High'),
        ('3', 'Critical'),
        ], default='0', index=True, string="Priority", track_visibility='onchange')
    epic_id=fields.Char('Epic ID', track_visibility='onchange')
    #'end_date': fields.date('End Date'),
    #'sprint_id': fields.many2one('project.sprint','Sprint'),
    billable=fields.Boolean('Billable', track_visibility='onchange')
    status=fields.Selection([('open','Open'),('inprogress','In Progress'),('re-open','Re-Open'),('completed','Completed')],'Status', track_visibility='onchange')
    start_date=fields.Date("Start Date", track_visibility='onchange')
    end_date=fields.Date("End Date", track_visibility='onchange')


    # -------------Code Updated for testing team-------------
    project_id = fields.Many2one('project.project',
        string='Project',
        default=lambda self: self.env.context.get('default_project_id'),
        index=True,
        required=True,
        track_visibility='onchange',
        change_default=True)
    id=fields.Integer('Task/Bug ID',readonly=True,track_visibility='onchange')
    user_id =fields.Many2one('res.users','Assigned to',track_visibility='onchange', default=False)
    rasised_by = fields.Many2one('res.users',
        string='Raised By',
        default=lambda self: self.env.uid,
        index=True, track_visibility='always')
    # assigned_to=fields.Many2one('res.users','Assigned To')
    detected_in_sprint=fields.Char('Detected In Sprint', track_visibility='onchange')
    build_no = fields.Float(string="Build No.", track_visibility='onchange')
    detected_build = fields.Float(string="Detected In Build", track_visibility='onchange')
    user_story=fields.Char("User Story", track_visibility='onchange')

    # ------------------------------------------------------
    # assigned_to=fields.Many2one('res.users','Assigned To')
    # detected_in_sprint=fields.Integer('Detected In Sprint')
    fixed_in_sprint=fields.Many2one('project.sprint','Fixed In Sprint', track_visibility='onchange')
    fixed_sprint=fields.Integer('Fixed Sprint', readonly=True, track_visibility='onchange')
    no_of_tests_impacted= fields.Integer('No of Tests Impacted', track_visibility='onchange')
    severity= fields.Selection([('critical', 'Critical'),('high', 'High'),('medium', 'Medium'),('low', 'Low')] ,'Severity', track_visibility='onchange')
    fixed_in_build= fields.Integer('Fixed In Build', track_visibility='onchange')
    issue_type=fields.Selection([('defect', 'Defect'),('enhancement', 'Enhancement'),('duplicate', 'Duplicate'),('not an issue', 'Not an issue')] ,'Issue Type', track_visibility='onchange')
    issue_status=fields.Selection([('open', 'Open'),('in progress', 'In Progress'),('complete', 'Complete'),('re-open', 'Re-Open'),('closed', 'Closed'),('deffered', 'Deffered'),('awaiting response', 'Awaiting Response')] ,'Issue Status', track_visibility='onchange')
    email_id=fields.Char("Email-Id")
    # root_cause=fields.Char("Root Cause")


    @api.onchange('project_id')
    def onchange_project(self):
    	# pdb.set_trace()
    	values = {}
    	module_list=[]
    	if self.project_id:
    		rec=self.env['project.modules'].search([('project_id','=', self.project_id.id)])
    		if rec:
    			for i in rec:
    				module_list.append(i.id)
    	return {'domain':{'module_id': [('id', 'in', module_list)]}}
    @api.onchange('module_id')
    def change_submodule_id(self):
    	# pdb.set_trace()
    	submodule_obj=self.env['project.modules.line']
    	get_rec=submodule_obj.search([('project_modules_id', '=', self.module_id.id),])
    	res=[]
    	if get_rec:
    		for rec in get_rec:
    			res.append(rec.id)
    	return {'domain':{'submodule_id': [('id', 'in', res)],}}

    @api.onchange('user_id')
    def change_assigned_to(self):
    	# pdb.set_trace()
    	if self.user_id:
    		self.email_id=self.user_id.login



# class project_extended_issue(models.Model):
#     _inherit = "project.issue"

#     _columns = {
#         'build_number': fields.integer('Build Number'),
#         'raised_by':fields.many2one('res.users','Raised By'),
#         'sprint_id': fields.many2one('project.sprint','Sprint'),
#         'detected_in_sprint': fields.integer('Detected In Sprint'),
#         'fixed_in_sprint': fields.integer('Fixed In Sprint'),
#         'no_of_tests_impacted': fields.integer('No of Tests Impacted'),
#         'severity': fields.selection([('critical', 'Critical'),('high', 'High'),('medium', 'Medium'),('low', 'Low')] ,'Severity'),
#         'priority': fields.selection([('critical', 'Critical'),('high', 'High'),('medium', 'Medium'),('low', 'Low')] ,'Priority',default='medium'),
#         'assigned_to': fields.many2one('res.users','Assigned to'),
#         'module': fields.char('Module'),
#         'detected_in_build': fields.integer('Detected In Build'),
#         'fixed_in_build': fields.integer('Fixed In Build'),
#         'issue_type': fields.selection([('defect', 'Defect'),('enhancement', 'Enhancement'),('duplicate', 'Duplicate'),('not an issue', 'Not an issue')] ,'Issue Type'),
#         'issue_status': fields.selection([('open', 'Open'),('in progress', 'In Progress'),('complete', 'Complete'),('re-open', 'Re-Open'),('closed', 'Closed'),('deffered', 'Deffered'),('awaiting response', 'Awaiting Response')] ,'Issue Status'),
#         'user_story': fields.selection([('gstr1st001','GSTR1ST001'),('high','GSTR1ST002'),('gstr1st003','GSTR1ST003'),('gstr1st004','GSTR1ST004'),('gstr1st005','GSTR1ST005'),('gstr1st006','GSTR1ST006'),('gstr1st007','GSTR1ST007'),('gstr1st008','GSTR1ST008'),('gstr1st009','GSTR1ST009'),('gstr1st0010','GSTR1ST0010'),('gstr1st0011','GSTR1ST0011'),('gstr1st0012','GSTR1ST0012')], 'User Story'),
#         'root_cause': fields.char('Root Cause'),
#     }

# class project_extended_sprint(models.Model):
#     _inherit = "project.sprint"

#     _columns = {
#         'project_id': fields.many2one('project.project','Project Name', required=True),
#         'module_id': fields.many2one('project.modules','Module'),
#         'submodule_id': fields.many2one('project.modules.line','Sub Module'),

#     }
#     @api.onchange('project_id')
#     def change_module_id(self):
#         module_obj=self.env['project.modules']
#         get_rec=module_obj.search([('project_id', '=', self.project_id.id),])
#         res=[]
#         if get_rec:
#              for rec in get_rec:
#                   res.append(rec.id)
#         return {
#               'domain': {
#                     'module_id': [('id', 'in', res)],
#            } }
#     @api.onchange('module_id')
#     def change_submodule_id(self):
#         submodule_obj=self.env['project.modules.line']
#         get_rec=submodule_obj.search([('project_modules_id', '=', self.module_id.id),])
#         res=[]
#         if get_rec:
#              for rec in get_rec:
#                   res.append(rec.id)
#         return {
#               'domain': {
#                     'submodule_id': [('id', 'in', res)],
#            } }
