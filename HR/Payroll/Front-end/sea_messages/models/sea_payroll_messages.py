from odoo import models, fields, api

class SeaPayrollMessages(models.Model):
    _name = 'sea.payroll.messages'
    _rec_name = 'emp_name'


    contract_id = fields.Many2one('hr.contract', string = 'Contract Name')
    emp_name = fields.Many2one('hr.employee', string = 'Employee Name')
    payroll_month = fields.Date(string = 'Payroll Month')
    message = fields.Char(string = 'Message')
    message_type = fields.Selection([('E','Error'),('W','Warning'),('I','Information')], string="Message Type")

   