# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import pdb
class project_task(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _compute_subtask_count(self):
        for task in self:
            task.subtask_count = self.search_count([('id', 'child_of', task.id), ('id', '!=', task.id),('task_type','=','task')])


    @api.multi
    def _compute_issue_count(self):
        for task in self:
            task.issue_count = self.search_count([('id', 'child_of', task.id), ('id', '!=', task.id),('task_type','=','issue')])

    task_type=fields.Selection([('task', 'Task'),('issue', 'Issue'),],String="Type",required=True,)
    issue_count = fields.Integer(compute='_compute_issue_count', type='integer', string="Sub-task count")
