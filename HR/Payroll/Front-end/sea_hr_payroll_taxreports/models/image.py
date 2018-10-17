# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _

class Extend_Employee(models.Model):
	_inherit = 'hr.employee'

	ip_number=fields.Char(string='ESI Number')
	uan		=fields.Char(string = 'PF Number')
	last_day=fields.Char(string='Last Working Day')
	reason_code=fields.Many2one('hr.code', string='Reason Code')

class Extend_Employee(models.Model):
	_name = 'hr.code'
	_rec_name='reason'

	code=fields.Integer(string='Code')
	reason=fields.Char(string='Reason')
