# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
#_logger = logging.getLogger(__name__)

class ideas(models.Model):
    _name = 'ideas.ideas'
    _inherit = ['mail.thread']
    _rec_name = 'idea_title'

    name = fields.Char(string='Idea', readonly=True)
    date = fields.Date(string="Date", default=fields.Datetime.now, readonly=True, store=True)
    idea_initiator = fields.Many2one('res.users','Idea Initiator', default=lambda self: self.env.user, required=True)
    idea_title = fields.Char(string="Idea Title", help="Give a Title to Your Idea", limit=[('val', '<=', 50)], required=True)
    pain_area = fields.Text(required=True)
    idea_source	 = fields.Text(string='Ideas Source', required=True)
    suggested_solution = fields.Text(string='Suggestions', required=True)
    column_one = fields.Char(domain="[('visible','=', False)]")
    column_two = fields.Char()
    tags_id = fields.Char()
    # tag_ids_one = fields.Char()
    # tag_ids_two = fields.Char()
    category = fields.Many2one('ideas.collect', string="Category", help='Sailotech IT, Sailotech Non-IT, CSR, Social Other than CSR, Others')
    outcome_of_idea = fields.Many2one('ideas.outcome', string="Outcome Of Idea", help='Mobile App, Custom solution in Oracle, Custom solution in Infor, Independent Custom Application, Solution in Sailotech ERP, Others')
    Prerequisites = fields.Text(help="Prerequisites for Solution to be Offered")
    business_benefit = fields.Text()
    next_step = fields.Char(limit=50)
    idea_status = fields.Selection([('A','Accepted'),('R','Rejected'),('P','Pending IRC Review'),('O','Open'),('D','Duplicate')], default='O')
    created_by = fields.Many2one('res.users','Created By', default=lambda self: self.env.user, readonly=True)
    update_by = fields.Many2one('res.users', string='Updated By')
    duplicate_idea = fields.Many2one('ideas.ideas', 'duplicate_idea', String="Duplicate iDea")
    #related_idea = fields.Char(string="Related Idea", help="If this Idea is related to another idea but is not duplicate.")
    related_idea = fields.Many2many('ideas.related', 'related_idea', String="Related Idea", help='If this Idea is related to another idea but is not duplicate.')
    tag_ids = fields.Many2many('ideas.tags', string="Tags")
    employee = fields.Many2one('hr.employee')
    # 'employee_category_rel', 'category_id', 'emp_id'
    remarks = fields.Text()

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('ideas.ideas') or '/'
        vals['name'] = seq
        return super(ideas, self).create(vals)

    # @api.onchange('category')
    # def onchange_section_id(self):
    #     if self.category:
    #         self.outcome_of_idea = self.category.outcome_of_idea

    def _employee_get(self):
        emp_id = self.env.context.get('default_employee_id', True)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return True

    defaults = {
        'employee_id': _employee_get,
        }

    @api.onchange('idea_initiator')
    def onchange_skill(self):
        if self.name:
            self.created_by=self.employee.update_by
#############################################################################################################################################################################################################################################################

class ideasgenerator(models.Model):
	_name = 'ideas.tags'
	_rec_name = 'tags'

	tags = fields.Char()
#############################################################################################################################################################################################################################################################

class ideascollect(models.Model):
    _name = 'ideas.collect'
    _rec_name = 'category'

    category = fields.Char()
#############################################################################################################################################################################################################################################################

class ideasoutcome(models.Model):
    _name = 'ideas.outcome'
    _rec_name = 'outcome_of_idea'

    outcome_of_idea = fields.Char()
#############################################################################################################################################################################################################################################################    

class ideasduplicate(models.Model):
    _name = 'ideas.duplicate'
    _rec_name = 'duplicate_idea'

    duplicate_idea = fields.Char()
#############################################################################################################################################################################################################################################################    

class ideasrelated(models.Model):
    _name = 'ideas.related'
    _rec_name = 'related_idea'

    related_idea = fields.Char()
