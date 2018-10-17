# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
import pdb

class project_modules(models.Model):
     _name = 'project.modules'
     #_inherit = 'project.issue'


     name = fields.Char("Module")
     description = fields.Text("Description")
     project_id = fields.Many2one("project.project", "Project")
     module_line_id=fields.One2many('project.modules.line','project_modules_id','Sub Modules Line')

     #     value2 = fields.Float(compute="_value_pc", store=True)
     #     description = fields.Text()
     #     @api.depends('value')
     #     def _value_pc(self):
     #         self.value2 = float(self.value) / 100

class project_modules_lines(models.Model):

     _name='project.modules.line'

     name=fields.Many2one('submodules',string='Sub Modules',track_visibility='onchange',store=True,)
     description=fields.Text("Description")
     project_modules_id=fields.Many2one('project.modules','Project Modules Id')


     @api.multi
     @api.onchange('name')
     def on_change_company_id(self):
          if self.name:
               # pdb.set_trace()
               self.description=self.name.description