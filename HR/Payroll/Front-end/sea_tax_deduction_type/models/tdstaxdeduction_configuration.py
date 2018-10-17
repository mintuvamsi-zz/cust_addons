
from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
import uuid

from itertools import groupby
from datetime import datetime, timedelta, time
from odoo.tools import DEFAULT_SERVER_TIME_FORMAT

from werkzeug.urls import url_encode

from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp

class taxdeductiontype(models.Model):
	_name = 'tds.taxdeductiontypes'
	_rec_name='deduction_desc'

	sectiontypes = fields.Char(string='Section',store= True)
	deduction_desc = fields.Char(string='Deduction Description',store= True)
	deduction_limit = fields.Integer(string='Deduction Limit',store= True)
	deductionlimit_type = fields.Selection([('F','Fixed Amount'),('C','Calculated Amount'),('N','Non-Calculated')],  string='Deduction Limit Type')
	limit_level = fields.Selection([('S','Section'),('I','Individual')],  string='Limit Level')

	
	# name = fields.Char('Badge Number', readonly=True)

	# @api.model
 #    def create(self, vals):
 #        seq = self.env['ir.sequence'].next_by_code('tds.taxdeductiontypes') or '/'
 #        vals['name'] = seq
 #        return super(taxdeductiontype, self).create(vals)