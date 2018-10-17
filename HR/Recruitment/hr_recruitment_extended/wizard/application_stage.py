import time
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError
from openerp.tools.translate import _
from datetime import datetime
import pdb

class application_status(models.TransientModel):
	_name = 'application.status'
# _inherit = "hr.applicant"

	application_status = fields.Char('Application Status')

