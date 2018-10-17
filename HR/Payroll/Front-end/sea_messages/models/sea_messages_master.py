from odoo import models, fields, api

class SeaMessagesMaster(models.Model):
	_name = 'sea.messages.master'
	_rec_name = 'message'


	# msg_id = fields.Integer(string = 'Message ID')
	msg_code = fields.Char(string = 'Message Code')
	message = fields.Text(string = 'Message')
	remarks = fields.Char(string = 'Remarks')