# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class submodules(models.Model):
     _name = 'submodules'
     #_inherit = 'project.issue'

     name = fields.Char("Sub Module")
     description = fields.Text("Description")
     module_line_id=fields.One2many('project.modules.line','project_modules_id','Sub Modules Line')