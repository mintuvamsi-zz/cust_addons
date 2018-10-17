# -*- coding: utf-8 -*-

from odoo import fields, models, api


class visitorconfigsetting(models.Model):
    _name = 'visitors.config.settings'
    _rec_name = 'email'

    #name = fields.Many2one('visitors.visitors',string='Name')
    email = fields.Char(string='E-mail')


    # resource_calendar_id = fields.Many2one(
    #     'resource.calendar', 'Company Working Hours')
    # module_hr_org_chart = fields.Boolean(string="Show Organizational Chart")
