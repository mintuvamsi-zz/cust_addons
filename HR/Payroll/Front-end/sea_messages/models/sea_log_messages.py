from odoo import models, fields, api

class SeaMessagesMaster(models.Model):
    _name = 'sea.log.messages'
    _rec_name = 'message_desc'

    contract_id = fields.Integer('Contract Name')
    function_name = fields.Char('Function')
    message_desc= fields.Char('Message Description')
    message_value= fields.Char('Message Value')
    location = fields.Integer('Location')