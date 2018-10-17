from odoo import api, fields, models, _

class TraceabilityMatrix(models.Model):
	_name = 'traceability.matrix'
	_rec_name = 'project_name'

	project_name = fields.Many2one('project.project', string='Project Name')
	author=fields.Many2one('hr.employee', string='Author')
	iteration_release=fields.Char('Iteration/Release')
	date_creation=fields.Date('Date of Creation')
	tower_name=fields.Char('Tower Name')
	responsible=fields.Many2one('hr.employee',string ='Responsible')
	matrix_line= fields.Char(string ='Responsible')
	matrix_line_id=fields.One2many('traceability.matrix.line', 'module_id', string='History')
	link_line_id=fields.One2many('traceability.matrix.line', 'module_id', string='History')
	test_line_id=fields.One2many('traceability.matrix.line', 'module_id', string='History')
	auto_line_id=fields.One2many('traceability.matrix.line', 'module_id', string='History')


class TraceabilityModule(models.Model):
	_name = 'traceability.module'
	_rec_name = 'module_name'

	module_name=fields.Char('Module Name')
	matrix_line_id=fields.Many2one('traceability.matrix.line', invisible=False, string='Matrix Line ID')

class TraceabilityMatrixLine(models.Model):
	_name = 'traceability.matrix.line'
	_rec_name = 'module_id'

	module_id=fields.Many2one('traceability.module',string='Module Name',track_visibility='onchange', primary_key=True)
	sub_module_name=fields.Char('Sub-Module Name')
	technical_name=fields.Char('Technical Name')
	custom_module=fields.Selection([('1','YES'),('2','NO')],'Custom Module')
	responsible=fields.Many2one('hr.employee',string ='Responsible')
	current_status=fields.Char('Current Status')
	features_requirements=fields.Char('Features/ Customer Requirements')
	#requirements_specification=fields.Char('Requirements Specification')
	fsdname_link =fields.Char('FSD Link')
	tdname_link=fields.Char('TD Link')
	requirements_id=fields.Integer('Related Requirements ID')
	design_components=fields.Selection([('1','Modified'),('2','Existing')], string='Modified/Existing')
	unit_test_case_link=fields.Char('Unit Test Case Link')
	unit_test_results=fields.Char('Unit Test Results')
	svn_commits=fields.Selection([('1','YES'),('2','NO')],'SVN Commits')
	svn_folder_path=fields.Char('SVN Folder Path')
	svn_commit_date=fields.Date('SVN Commit Date')
	code_review=fields.Selection([('1','Completed'),('2','Pending'),('3','Not Required')],'Code Review')
	automation_status=fields.Selection([('1','Fail'),('2','Pass')],'Automation Status')
	automation_code_link=fields.Char('Automation Code Link')
	automation_results=fields.Char('Automation Results')
	integration_system_test_cases=fields.Char('Integration/ System Test Cases')
	integration_system_test_results=fields.Char('Integration/ System Test Results')
	user_manuals_link=fields.Char('User Manuals Link')
	democript=fields.Char('Demo Script')
	sales_decks=fields.Char('Sales Decks')
	last_updated_date=fields.Date('Last Updated Date')
	last_updated_by=fields.Many2one('hr.employee', string='Last Updated By')
	last_review_comments=fields.Char('Last Review Comments')
	last_reviewed_by=fields.Many2one('hr.employee', string='Last Reviewed By')
	last_review_date=fields.Date('Last Review Date')
