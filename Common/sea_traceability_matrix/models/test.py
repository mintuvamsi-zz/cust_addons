from odoo import api, fields, models, _
from datetime import datetime

class TraceabilityMatrix(models.Model):
    _name = 'traceability.matrix'
    _rec_name = 'project_name'
    _inherit = ['mail.thread']

    id=fields.Char(string='Related Requirements ID')

    #Traceability Matrix Header
    project_name = fields.Many2one('project.project', string='Project Name', track_visibility='onchange')
    author=fields.Many2one('hr.employee', string='Author', track_visibility='onchange')
    iteration_release=fields.Char('Iteration/Release', track_visibility='onchange')
    date_creation=fields.Date('Date of Creation',track_visibility='onchange',default=fields.Datetime.now(),readonly=True)
    tower_name=fields.Many2one('tower.name', string='Tower Name',track_visibility='onchange')
    responsible=fields.Many2one('hr.employee',string ='Tower Owner',track_visibility='onchange')
    last_updated_date1=fields.Date('Last Updated Date',track_visibility='onchange',default=fields.Datetime.now())

    #General
    module_id=fields.Many2one('module.id', string='Module Name',track_visibility='onchange')
    sub_module_name=fields.Many2one('sub.module.name', string='Sub-Module Name',track_visibility='onchange')
    technical_name=fields.Char(string='Technical Name',track_visibility='onchange')
    custom_module=fields.Selection([('1','Custom Module'),('2','Base Module')],'Module Type',track_visibility='onchange')
    responsible_line=fields.Many2one('hr.employee',string ='Responsible',track_visibility='onchange',default=lambda self: self.env.user, readonly=True)
    current_status=fields.Selection([('1','Completed'),('2','Pending'),('3','Ready'),('4','In Progress')], string='Current Status' ,track_visibility='onchange', default='2')

    #Functional
    #functional_testing
    features_requirements=fields.Text(string='Features/ Customer Requirements',track_visibility='onchange', limit=150)
    requirements_specification=fields.Text(string='Requirements Specification',track_visibility='onchange', limit=150)        
    fsdname_link =fields.Char('FSD Link',track_visibility='onchange')
    fsd_status=fields.Selection([('1','Completed'),('2','Pending'),('3','Not Required'),('4','In Progress')],'Functional Document',track_visibility='onchange', default='2')     
    fsdname =fields.Char('FSD Name',track_visibility='onchange')
    fsd_review=fields.Many2one('hr.employee', 'FSD Reviewed By')
    fsd_review_date=fields.Date('FSD Review Date',track_visibility='onchange')
    fsd_review_com=fields.Text('FSD Review Comments', limit=50,track_visibility='onchange')
    #requirements_id=fields.Integer('Related Requirements ID',track_visibility='onchange')
    fsd_last_updated_date=fields.Date('Last Updated Date',track_visibility='onchange',default=fields.Datetime.now())
    fsd_last_updated_by=fields.Many2one('hr.employee', string='Last Updated By',track_visibility='onchange', default=lambda self: self.env.user)
    fsd_rev=fields.Selection([('1','Completed'),('2','Pending'),('4','In Progress')],'FSD Review',track_visibility='onchange',default='2')

    #Technical
    tdname_link=fields.Char('TD Link')
    tdname=fields.Char('TD Name')
    td_review=fields.Selection([('1','Completed'),('2','Pending'),('4','In Progress')],'TD Review',track_visibility='onchange',default='2')
    td_reviewed=fields.Many2one('hr.employee','TD Reviewed By')
    td_reviewed_com=fields.Text('TD Review Comments', limit=150)
    unittest_status=fields.Selection([('1','Completed'),('2','Pending'),('3','Not Required'),('4','In Progress')],'Unit Test Document',track_visibility='onchange', default='2')
    td_reviewed_date=fields.Date('TD Review Date')
    design_components=fields.Selection([('1','Modified'),('2','Existing')], string='Modified/Existing',track_visibility='onchange')
    unit_test_case_link=fields.Char('Unit Test Document Link',track_visibility='onchange')
    unit_test_results=fields.Selection([('1','Passed'),('2','Failed'),('3','In Progress')], 'Unit Test Results',track_visibility='onchange',default='3')
    svn_commits=fields.Selection([('1','YES'),('2','NO')],'SVN Commits',track_visibility='onchange', default='2')
    svn_folder_path=fields.Char('SVN Folder Path',track_visibility='onchange') 
    svn_commit_date=fields.Date('SVN Commit Date',track_visibility='onchange')  
    code_review=fields.Selection([('1','Completed'),('2','Pending'),('3','Not Required'),('4','In Progress')],'Code Review',track_visibility='onchange',default='2') 
    code_reviewed_by=fields.Many2one('hr.employee', string='Code Reviewed By',track_visibility='onchange')
    code_reviewed_date=fields.Date(string='Code Review Date',track_visibility='onchange')
    code_review_com=fields.Text('Code Review Comments', limit=150, track_visibility='onchange')
    td_status=fields.Selection([('1','Completed'),('2','Pending'),('3','Not Required'),('4','In Progress')],'Technical Document',track_visibility='onchange', default='2') 
    td_last_updated_date=fields.Date('TD Last Updated Date',track_visibility='onchange',default=fields.Datetime.now())
    td_last_updated_by=fields.Many2one('hr.employee', string='TD Last Updated By',track_visibility='onchange', default=lambda self: self.env.user)
    svn_last_updated_date=fields.Date('SVN Last Updated Date',track_visibility='onchange',default=fields.Datetime.now())
    svn_last_updated_by=fields.Many2one('hr.employee', string='SVN Last Updated By',track_visibility='onchange', default=lambda self: self.env.user)

    #QA
    automation_status=fields.Selection([('1','Completed'),('2','Pending'),('3','Not Required'),('4','In Progress')],'Automation Status',track_visibility='onchange',default='2')
    automation_code_link=fields.Char('Automation Code Link',track_visibility='onchange')    
    automation_results=fields.Selection([('1','Passed'),('2','Failed'),('3','In Progress')], string='Automation Results',track_visibility='onchange',default='3')      
    integration_system_test_cases=fields.Char('Integration/ System Test Cases',track_visibility='onchange')
    integration_system_test_results=fields.Selection([('1','Passed'),('2','Failed'),('3','In Progress')], 'Integration/ System Test Results',track_visibility='onchange')
    qa_tested_by=fields.Many2one('hr.employee', string='Tested By',track_visibility='onchange')
    qa_reviewed_by=fields.Many2one('hr.employee', string='Reviewed By',track_visibility='onchange')
    qa_reviewed_date=fields.Date(string='Review Date',track_visibility='onchange')
    qa_review_com=fields.Text('Review Comments', limit=150, track_visibility='onchange')
    qa_last_updated_date=fields.Date('Last Updated Date',track_visibility='onchange',default=fields.Datetime.now())
    qa_last_updated_by=fields.Many2one('hr.employee', string='Last Updated By',track_visibility='onchange', default=lambda self: self.env.user)


    #Management
    user_manuals_link=fields.Char('User Manuals Link',track_visibility='onchange')
    democript=fields.Char('Demo Script',track_visibility='onchange')
    sales_decks=fields.Char('Sales Decks',track_visibility='onchange')   
    

    #Misc
    #last_updated_date=fields.Date('Last Updated Date',track_visibility='onchange',default=fields.Datetime.now())
    #last_updated_by=fields.Many2one('hr.employee', string='Last Updated By',track_visibility='onchange', default=lambda self: self.env.user) 
    last_review_comments=fields.Text('Last Review Comments',track_visibility='onchange', limit=200)             
    last_reviewed_by=fields.Many2one('hr.employee', string='Last Reviewed By',track_visibility='onchange')
    last_review_date=fields.Date('Last Review Date',track_visibility='onchange')

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('traceability.matrix') or '/'
        vals['id'] = seq
        return super(TraceabilityMatrix,self).create(vals)


class TraceabilityTags(models.Model):
    _name = 'module.id'
    _inherit = ['mail.thread']
    _rec_name = 'module_id'

    module_id=fields.Char(string='Module Name',track_visibility='onchange', primary_key=True)
    date=fields.Date('Date of Creation', default=fields.Datetime.now(), readonly=True)
    created_by=fields.Many2one('hr.employee',string ='Created By', default=lambda self: self.env.user, readonly=True)

class TraceabilityTags(models.Model):
    _name = 'sub.module.name'
    _inherit = ['mail.thread']
    _rec_name = 'sub_module_name'

    sub_module_name=fields.Char('Sub-Module Name',track_visibility='onchange', primary_key=True)
    date=fields.Date('Date of Creation', default=fields.Datetime.now(), readonly=True)
    created_by=fields.Many2one('hr.employee',string ='Created By',default=lambda self: self.env.user, readonly=True)


class TraceabilityTags(models.Model):
    _name = 'tower.name'
    _inherit = ['mail.thread']
    _rec_name = 'tower_name'

    tower_name=fields.Char('Tower Name',track_visibility='onchange', primary_key=True)
    date=fields.Date('Date of Creation', default=fields.Datetime.now(), readonly=True)
    created_by=fields.Many2one('hr.employee',string ='Created By',default=lambda self: self.env.user, readonly=True)