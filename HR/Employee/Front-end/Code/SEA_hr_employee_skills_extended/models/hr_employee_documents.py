# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging

from odoo import api, fields, models,_
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource
import pdb

_logger = logging.getLogger(__name__)


class hr_employee_skills(models.Model):
	_name= "hr.employee.skills"

	def _employee_get(self):
		#pdb.set_trace()
		emp_id = self.env.get('default_employee_id', False)
		if emp_id:
			return emp_id
		ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
		if ids:
			return ids[0].id





	name = fields.Many2one('hr.skills','Skills')
	skill_category = fields.Selection([
     				('technical', 'Technical'),('non-technical', 'Non-Technical')] ,
     		             string='Category')
	level= fields.Selection(string='Level',  selection=[('beginner', 'Beginner'),('intermediate', 'Intermediate'),('expert', 'Expert')])
	employee_id=fields.Many2one('hr.employee','Employee', default=_employee_get,readonly="1")
	years=fields.Char('Experience (In Years)')




	@api.onchange('name')
	def onchange_skill(self):
		if self.name:
			self.skill_category=self.name.category
