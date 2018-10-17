# -*- coding: utf-8 -*-

from odoo import models, fields, api

class chartofaccountshierarchy(models.Model):
    _inherit = ['account.account']

    parent_account = fields.Many2one('account.group')
    


 #########################################################################################################################################

# class accounthierarchy(models.Model):
# 	_name = 'account.hierarchy'
# 	_inherit = 'account.group'

# 	parent_account = fields.Char(string="Parent")

# 	@api.depends('parent_id')
#     def _value_pc(self):
#     	self.parent_account = Char(self.account.group.parent_id) 

