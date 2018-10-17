import logging

import openerp
from openerp import api
from openerp import SUPERUSER_ID
from datetime import datetime
from openerp import tools
from openerp.modules.module import get_module_resource
from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare
import datetime
from datetime import timedelta
import calendar
from ast import literal_eval
from dateutil import relativedelta
from openerp.tools.translate import _
import re
_logger = logging.getLogger(__name__)
import pdb

class appraisal_cron(osv.Model):

    _name = "appraisal.cron"
    _description = "Appraisal Cron"



    def period_cron(self,cr,uid,context=None):

    	appraisal_obj=self.pool.get('employee.appraisal')
        appraisal_id=appraisal_obj.search(cr,uid,[])

    	for appr in appraisal_id:
            appr=appraisal_obj.browse(cr,uid,appr)
            
            if appr.appraisal_period_id.active_date:
                if datetime.datetime.strptime(appr.appraisal_period_id.active_date, "%Y-%m-%d").date() == datetime.datetime.now().date():
                    appr.appraisal_active=True
