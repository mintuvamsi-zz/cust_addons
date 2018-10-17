from odoo import models, fields, api
from datetime import datetime

class SeaMessagesMaster(models.Model):
    _name = 'sea.payroll.log.error'
    _rec_name = 'error_description'

    contract_id = fields.Many2one('hr.contract',"Contract Name")
    emp_id = fields.Many2one('hr.employee',"Employee Name")
    function_name = fields.Char("Function Name")
    error_location = fields.Integer("Error Location")
    error_description = fields.Text("Error Description")
    log_timestamp = fields.Date("Time")