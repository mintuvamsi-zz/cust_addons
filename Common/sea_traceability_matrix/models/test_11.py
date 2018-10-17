from odoo import api, fields, models, _
from datetime import datetime

class TraceabilityMatrix(models.Model):
    _name = 'traceability.matrix'
    _rec_name = 'project_name'
    _inherit = ['mail.thread']

    project_name = fields.Many2one('project.project', string='Project Name', track_visibility='onchange')
    author=fields.Many2one('hr.employee', string='Author', track_visibility='onchange')
    iteration_release=fields.Char('Iteration/Release', track_visibility='onchange')
    date_creation=fields.Date('Date of Creation',track_visibility='onchange',default=fields.Datetime.now(),readonly=True)
    tower_name=fields.Char('Tower Name',track_visibility='onchange')
    responsible=fields.Many2one('hr.employee',string ='Owner',track_visibility='onchange')
    #last_updated_date1=fields.Date(string='Last Updated Date', default=fields.Datetime.now())
    last_updated_date1=fields.Date('Last Updated Date',track_visibility='onchange',default=fields.Datetime.now())

    #General
    module_id=fields.Many2one('module.id', string='Module Name',track_visibility='onchange')
    sub_module_name=fields.Many2one('sub.module.name', string='Sub-Module Name',track_visibility='onchange')
    technical_name=fields.Many2one('technical.name', string='Technical Name',track_visibility='onchange')
    custom_module=fields.Selection([('1','YES'),('2','NO')],'Custom Module',track_visibility='onchange')
    responsible_line=fields.Many2one('hr.employee',string ='Responsible',track_visibility='onchange')
    current_status=fields.Many2many('current.status', string='Current Status',track_visibility='onchange')

    #Functional
    features_requirements=fields.Many2many('traceability.tags', string='Features/ Customer Requirements',track_visibility='onchange')
    requirements_specification=fields.Many2many('traceability.tags1', string='Requirements Specification',track_visibility='onchange')        
    fsdname_link =fields.Char('FSD Name & Link',track_visibility='onchange')
    requirements_id=fields.Integer('Related Requirements ID',track_visibility='onchange')

    #Technical
    tdname_link=fields.Char('TD Link')
    design_components=fields.Selection([('1','Modified'),('2','Existing')], string='Modified/Existing',track_visibility='onchange')
    unit_test_case_link=fields.Char('Unit Test Case Link',track_visibility='onchange')
    unit_test_results=fields.Char('Unit Test Results',track_visibility='onchange')
    svn_commits=fields.Selection([('1','YES'),('2','NO')],'SVN Commits',track_visibility='onchange')
    svn_folder_path=fields.Char('SVN Folder Path',track_visibility='onchange') 
    svn_commit_date=fields.Date('SVN Commit Date',track_visibility='onchange')  
    code_review=fields.Selection([('1','Completed'),('2','Pending'),('3','Not Required')],'Code Review',track_visibility='onchange') 
    
    
    #QA
    automation_status=fields.Selection([('1','Fail'),('2','Pass')],'Automation Status',track_visibility='onchange')
    automation_code_link=fields.Char('Automation Code Link',track_visibility='onchange')    
    automation_results=fields.Char('Automation Results',track_visibility='onchange')      
    integration_system_test_cases=fields.Char('Integration/ System Test Cases',track_visibility='onchange')
    integration_system_test_results=fields.Char('Integration/ System Test Results',track_visibility='onchange')


    #Management
    user_manuals_link=fields.Char('User Manuals Link',track_visibility='onchange')
    democript=fields.Char('Demo Script',track_visibility='onchange')
    sales_decks=fields.Char('Sales Decks',track_visibility='onchange')   
    

    #Misc
    last_updated_date=fields.Date('Last Updated Date',track_visibility='onchange')
    last_updated_by=fields.Many2one('hr.employee', string='Last Updated By',track_visibility='onchange') 
    last_review_comments=fields.Char('Last Review Comments',track_visibility='onchange')             
    last_reviewed_by=fields.Many2one('hr.employee', string='Last Reviewed By',track_visibility='onchange')
    last_review_date=fields.Date('Last Review Date',track_visibility='onchange')

class TraceabilityTags(models.Model):
    _name = 'traceability.tags'
    _rec_name = 'features_requirements'

    features_requirements=fields.Char('Features/ Customer Requirements')


class TraceabilityTags1(models.Model):
    _name = 'traceability.tags1'
    _rec_name = 'requirements_specification'

    requirements_specification=fields.Char('Requirements Specification') 

class TraceabilityTags(models.Model):
    _name = 'module.id'
    _rec_name = 'module_id'

    module_id=fields.Char(string='Module Name',track_visibility='onchange', primary_key=True)

class TraceabilityTags(models.Model):
    _name = 'sub.module.name'
    _rec_name = 'sub_module_name'

    sub_module_name=fields.Char('Sub-Module Name', primary_key=True)


class TraceabilityTags(models.Model):
    _name = 'technical.name'
    _rec_name = 'technical_name'

    technical_name=fields.Char('Technical Name', primary_key=True)

class TraceabilityTags(models.Model):
    _name = 'current.status'
    _rec_name = 'current_status'

    current_status=fields.Char('Current Status', primary_key=True)