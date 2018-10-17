import logging

import odoo
from openerp import api

from odoo import tools

from itertools import groupby
from datetime import datetime, timedelta
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)

class hr_employee_grade(models.Model):
    _inherit = 'hr.employee'

    grade= fields.Char("Grade")
    dod= fields.Date("Date of Designation")
    x_date_of_joining=fields.Date('Date of Joining')
