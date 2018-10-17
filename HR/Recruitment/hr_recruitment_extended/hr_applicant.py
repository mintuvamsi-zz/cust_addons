# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
import time
import pdb
import requests
class Applicant(models.Model):
    _inherit = "hr.applicant"


    summary_details = fields.One2many('summary.detail', 'applicant_rel', 'Summary Details')
    skill_set = fields.Text("Skill Matrix")
    current_ctc = fields.Char("Current CTC")
    notice_period = fields.Char("Notice Period")
    current_company = fields.Char("Current Company")
    current_location = fields.Char("Current Location")
    preffered_location = fields.Char("Preffered Location")
    priority = fields.Selection(selection_add=[('poor','Poor')])
    requisition=fields.Many2one('job.requisition', 'Requisition')


class summary_detail(models.Model):
    _description = "Application Summary Details"
    _name = 'summary.detail'

    name = fields.Char("Feedback")
    date = fields.Datetime("Date")
    by_user = fields.Many2one('res.users', "By")
    # responisible = fields.Many2one('res.users', "Responisible")
    next_responsible = fields.Many2one('res.users', string='Next Responsible')
    applicant_rel = fields.Many2one('hr.applicant')


