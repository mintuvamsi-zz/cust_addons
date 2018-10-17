# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hr_skills(models.Model):
     _name = 'hr.skills'

     name = fields.Char("Skill Name", required=True);
     category = fields.Selection([
     	('technical', 'Technical'),('non-technical', 'Non-Technical')] ,
     	"Category");
     parent = fields.Many2one("hr.skills","Parent Skill/Skill Group ")
     
