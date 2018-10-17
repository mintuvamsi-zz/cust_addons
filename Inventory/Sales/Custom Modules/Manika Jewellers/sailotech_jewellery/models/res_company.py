from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    active_serial_num = fields.Boolean(string="Active Serial Number")