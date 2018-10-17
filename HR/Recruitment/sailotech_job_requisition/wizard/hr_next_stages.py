import time
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import UserError
from openerp.tools.translate import _
from datetime import datetime
import pdb

class next_summary_details(models.TransientModel):
    _name = 'next.summary.details'
    _inherit = ['mail.thread']

    next_responsible = fields.Many2one('res.users', string='Next Responsible' , required=True)
    
    stage_id = fields.Many2one('hr.recruitment.stage', 'Stage',required=True,)
    observation = fields.Text('Remarks',required=True)
    
    @api.multi
    def button_subbmit(self):       
        wizard_active_id = self.env.context.get('active_id', False)
        hr_applicant_obj = self.env['hr.applicant'].browse(wizard_active_id)    
        logged_user = self.env.context['uid']

        if self.observation and self.stage_id:
            summary_details_obj=self.env['summary.detail']
            applicant_vals = {}
            current_date = str(datetime.now().date())
            # current_date = fields.datetime.now()
            applicant_vals.update({'by_user': logged_user,
                                   'name': self.observation,
                                   'applicant_rel':wizard_active_id,
                                   'date':datetime.strptime(current_date, "%Y-%m-%d"),                                   
                                   })      
            hr_applicant_obj.stage_id = self.stage_id.id
            hr_applicant_obj.user_id = self.next_responsible
            summary_details_obj.create(applicant_vals)
        return True
         

        