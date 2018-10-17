# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp
from openerp.tools.float_utils import float_compare
import datetime
from datetime import timedelta
import calendar

from dateutil import relativedelta

import re
import pdb


class appraisal_periodic_category(models.Model):

    _name = "appraisal.periodic.category"
    _description = "Appraisal Category"

    name= fields.Char('Appraisal Period', required=True, track_visibility='onchange')
    date_from=fields.Date('Date From', track_visibility='onchange')
    date_to=fields.Date('Date To', track_visibility='onchange')
    active= fields.Boolean('Active', track_visibility='onchange')
    active_date=fields.Date('Active Date',)


    _defaults = {
        'color_name': 'red',
        'active': True,
    }

    @api.multi
    @api.onchange('date_to')
    def onchange_active_date(self):
        if self.date_to:
            # pdb.set_trace()
            date_1 = datetime.datetime.strptime(self.date_to, "%Y-%m-%d")
            edit_date = date_1 - datetime.timedelta(days=20)
            self.active_date=edit_date.strftime('%Y-%m-%d')



class employee_appraisal(models.Model):
    _name = "employee.appraisal"
    _description = "Employee"

    _inherit = ['mail.thread',]



    @api.depends('employee_rating_id.self_rating','employee_rating_id.manager_rating')
    def _avg_jr_rating(self):
        """
        Compute the total amounts of the SO.
        """
        leng_rating=len(self.employee_rating_id)
        if leng_rating !=0 :
            for rating in self:
                emp_tot_rating = self_rating = manager_rating = 0
                for line in rating.employee_rating_id:
                    self_rating += line.self_rating
                    manager_rating += line.manager_rating
                    # return self_rating
                rating.update({
                     # 'self_rating':rating.round(self_rating),
                     # 'manager_rating':rating.round(manager_rating),
                    'emp_avg_jr_rating':float(self_rating) / leng_rating ,
                    'mng_avg_jr_rating':float(manager_rating) / leng_rating
                    })



    @api.depends('employee_job_requirement_id.emp_rating','employee_job_requirement_id.man_rating')
    def _avg_kra_rating(self):
        """
        Compute the total amounts of the SO.
        """
        leng_rating=len(self.employee_job_requirement_id)
        if leng_rating !=0 :
            for rating1 in self:
                emp_tot_rating = emp_rating = man_rating = 0
                for line in rating1.employee_job_requirement_id:
                    emp_rating += line.emp_rating
                    man_rating += line.man_rating
                rating1.update({
                    'emp_avg_kra_rating':float(emp_rating) / leng_rating ,
                    'mng_avg_kra_rating':float(man_rating) / leng_rating
                    })



    def _get_total(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = (line.mng_avg_jr_rating + line.mng_avg_kra_rating)/2
        return res


    @api.depends('employee_job_requirement_id.weightage')
    def _tot_weightage(self):
        """
        Compute the total amounts of the SO.
        """
        leng_weightage=len(self.employee_job_requirement_id)
        for total in self:
            emp_tot_weightage = weightage = 0
            for line in total.employee_job_requirement_id:
                weightage += line.weightage
            total.update({
                'total_weightage':weightage
                })


    #we need a related field in order to be able to sort the employee by name
    name= fields.Many2one('hr.employee', 'Employee Name',track_visibility='onchange')
    state=fields.Selection([('draft', 'Draft Appraisal'),('to_emp','Send to Employee'),
        ('sent', 'Sent to Manager'),
        ('to_approve', 'Sent to HR'),
        ('to_md','Sent to MD'),
        ], string='Status',readonly=True, index=True,copy=False, track_visibility='onchange')
    appraisal_period_id=fields.Many2one('appraisal.periodic.category','Appraisal Period', track_visibility='onchange')
    location= fields.Char('Location', track_visibility='onchange')
    designation= fields.Many2one('hr.job','Designation',track_visibility='onchange')
    user_id=fields.Many2one('res.users',related='name.user_id',string='Users',store=True, track_visibility='onchange')
    doj= fields.Date("Date of Joining",track_visibility='onchange')
    department_id=fields.Many2one('hr.department','Department',track_visibility='onchange')
    reviewers_name= fields.Many2one('hr.employee','Reviewers Name',track_visibility='onchange')
    todays_date=fields.Date(string='Date', default=datetime.datetime.today() , track_visibility='onchange')
    appraisal_active=fields.Boolean('Appraisal Active')
    emp_tot_rating=fields.Integer('Emp Tot Rating', track_visibility='onchange')
    emp_avg_jr_rating=fields.Float(string='Emp JR Average Rating', compute='_avg_jr_rating', track_visibility='onchange')
    mng_avg_jr_rating=fields.Float(string='Manager JR Average Rating', compute='_avg_jr_rating', track_visibility='onchange')
    emp_avg_kra_rating=fields.Float(string='Employee KRA Average Rating', compute='_avg_kra_rating', track_visibility='onchange')
    mng_avg_kra_rating=fields.Float(string='Manager KRA Average Rating', compute='_avg_kra_rating', track_visibility='onchange')
    total_weightage=fields.Float(string='Total Weightage', compute='_tot_weightage', track_visibility='onchange')
    comments_by_hr=fields.Char('Comments By HR', track_visibility='onchange')
    comments_by_md=fields.Char('Comments By MD', track_visibility='onchange')
    employee_comment_set=fields.Boolean('Employee comment set', track_visibility='onchange')
    employee_rating_id=fields.One2many('employee.rating','appraisal_id','Appraisal', track_visibility='onchange')
        #'overall_rating':fields.function(_get_total, string='Overall Manager Rating', type='float', track_visibility='onchange'),
    overall_evaluation_of_performance=fields.Text('Overall Evaluation of Performance', track_visibility='onchange')
    time_in_current_position=fields.Char('Time in current position', track_visibility='onchange')
    time_with_company=fields.Char('Time with Company', track_visibility='onchange')
    date=fields.Date('Date', track_visibility='onchange')
    evaluation_list=fields.Selection([
        ('far_exceeds_expectation', 'Far Exceeds Expectations'),
        ('exceed_expectation', 'Exceed Expectations'),
        ('met_expectation', 'Met Expectations'),
        ('below_expectation','Below Expectations'),
        ('never_met','Never Met'),
        ], string='Overall Evaluation', index=True,copy=False, track_visibility='onchange')
    job_grade=fields.Char('Job Grade', track_visibility='onchange')
    current_salary=fields.Float('Current Salary')
    proposed_merit_increase=fields.Integer('Proposed Merit Increase (%)')
    proposed_salary=fields.Float('Proposed Salary')
    proposed_promotion_list=fields.Selection([
        ('yes','Yes'),
        ('no','No'),
        ], string='Proposed Promotion', index=True,copy=False)
    proposed_designation=fields.Char('Proposed Designation')
    employee_job_requirement_id=fields.One2many('employee.job.requirement','job_requirement_id','Job Requirement', track_visibility='onchange')



    @api.one
    @api.constrains('total_weightage')
    def _total_weightage(self):
        record = self.total_weightage
        if record.total_weightage == 100:
            return True
        else:
            raise ValidationError(_("Error: Total Weightage should be equal to 100"))
        return True




    @api.model
    def default_get(self,default_fields):
        res={}
        #pdb.set_trace()
        #res = super(employee_appraisal, self).default_get(fields)
        srd = self.env['employee.rating']
        ids=[]
        active_id = self._context.get('active_ids', [])
        items_list=self.env['rating.name'].search([])
        for item in items_list:
            result={'appraisal_id':active_id,'name':item.id,'state':'draft'}
            sr = srd.create(result)
            ids.append(sr.id)
        res['employee_rating_id'] = ids
        res['state']='draft'
        user = self.env['hr.employee'].search([('user_id','=',self.env.uid)])
        res['name']=user.id
        res['appraisal_period_id']=self.env['appraisal.periodic.category'].search([('active','=',"True")]).id
        return res

    @api.onchange('name')
    def onchange_employee_name(self):
        if self.name:
            self.doj=self.name.doj
            self.reviewers_name=self.name.parent_id.id
            self.department_id=self.name.department_id.id
            self.designation=self.name.job_id.id
            self.location=self.name.work_location
            self.job_grade=self.name.grade


    @api.multi
    def button_send_employee(self):
        if self.total_weightage==100:
            self.state='to_emp'
            for line in self.employee_rating_id:
                line.state='to_emp'
            for line in self.employee_job_requirement_id:
                line.status='to_emp'
            template = self.env.ref('sailotech_employee_appraisal.employee_email_template')
            self.env['mail.template'].browse(template.id).send_mail(self.id)

            return True
        else:
            raise UserError(_('Error: Total Weightage should be equal to 100'))


    @api.multi
    def button_send_manager(self):
        records=self.employee_rating_id
        count_comment=0
        for record in records:
            if record.employee_comments:
                count_comment=count_comment+1
            else:
                raise UserError(_('Please Fill Employee Comments'))
        #pdb.set_trace()
        if len(self.employee_rating_id)==count_comment:
            self.state='sent'
            for line in self.employee_rating_id:
                line.state='sent'
            for line in self.employee_job_requirement_id:
                line.status='sent'
            template = self.env.ref('sailotech_employee_appraisal.manager_email_template')
            self.env['mail.template'].browse(template.id).send_mail(self.id)
            # pdb.set_trace()
            return True


    @api.multi
    def button_send_hr(self):
        records=self.employee_rating_id
        count_comment=0
        for record in records:
            if record.manager_comments:
                count_comment=count_comment+1
            else:
                raise UserError(_('Please Fill Managger Comments'))
        if len(self.employee_rating_id)==count_comment:
            self.state='to_approve'
            for line in self.employee_rating_id:
                line.state='to_approve'
            for line in self.employee_job_requirement_id:
                line.status='to_approve'
            template = self.env.ref('sailotech_employee_appraisal.hr_email_template')
            self.env['mail.template'].browse(template.id).send_mail(self.id)

    @api.multi
    def button_send_md(self):
        self.state='to_md'
        for line in self.employee_rating_id:
            line.state='to_md'
        for line in self.employee_job_requirement_id:
            line.status='to_md'
    @api.multi
    def button_back(self):
        if self.state=='to_approve':
            self.state='sent'
            for line in self.employee_rating_id:
                line.state='sent'
            for line in self.employee_job_requirement_id:
                line.status='sent'
        template = self.env.ref('sailotech_employee_appraisal.hr_reject_email_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id)


    @api.onchange('current_salary','proposed_merit_increase')
    def onchange_proposed_salary(self):
        pro_merit= float(self.proposed_merit_increase)
        if self.current_salary or pro_merit:
            self.proposed_salary = self.current_salary + (self.current_salary * (pro_merit/100))


    @api.onchange('date')
    def onchange_date_diff(self):
        # pdb.set_trace()
        if self.date:
            fmt = '%Y-%m-%d'
            d1 = datetime.datetime.strptime(self.name.doj, fmt)
            d2 = datetime.datetime.strptime(self.date, fmt)
            Diff=relativedelta.relativedelta(d2, d1)
            self.time_with_company=str(Diff.years)+" Years "+str(Diff.months)+" Months " +str(Diff.days)+ " Days "


    @api.onchange('date')
    def onchange_time_in_current_position(self):
      # pdb.set_trace()
       if self.date:

          fmt = '%Y-%m-%d'
          if self.name.dod:
            d1 = datetime.datetime.strptime(self.name.dod, fmt)
            d2 = datetime.datetime.strptime(self.date, fmt)
            Diff=relativedelta.relativedelta(d2, d1)
            self.time_in_current_position=str(Diff.years)+" Years "+str(Diff.months)+" Months " +str(Diff.days)+ " Days "


class employee_rating(models.Model):
    _name = "employee.rating"
    _description = "Part A"
    _inherit = ['mail.thread',]



    state=fields.Selection([('draft', 'Draft Appraisal'),('to_emp', 'Send to Employee'),('sent', 'Sent to Manager'),('to_approve', 'Sent to HR'),('to_md','Sent to MD'),],
    string='Status', store=True,track_visibility='onchange')
    appr_active_rel= fields.Boolean(related='appraisal_id.appraisal_active',string='Appraisal Active Related',store=True)
    name=fields.Many2one('rating.name', 'Job Requirement',track_visibility='onchange')
    self_rating=fields.Integer('Self Rating', track_visibility='onchange')
    employee_comments=fields.Char('Employee Comments', track_visibility='onchange')
    manager_rating= fields.Float('Manager Rating', track_visibility='onchange')
    manager_comments= fields.Char('Manager Comments', track_visibility='onchange')
    appraisal_id=fields.Many2one('employee.appraisal','Appraisal Id', track_visibility='onchange')


    @api.one
    @api.constrains('self_rating')
    def _self_rating(self):
        record = self
        if record.self_rating<=5 and record.self_rating>=1:
            return True
        else:
            raise ValidationError(_('Error: Invalid JR Employee Rating'))
        return True
    @api.one
    @api.constrains('manager_rating')
    def _manager_rating(self):
        record = self

        if record.manager_rating<=5 and record.manager_rating>=1:
            return True
        else:
            raise ValidationError(_('Error: Invalid JR Manager Rating'))
        return True




class rating_name(models.Model):
    _name = 'rating.name'

    name=fields.Char('Job Requirement', track_visibility='onchange')



class employee_job_requirement(models.Model):
    _name = "employee.job.requirement"
    _description = "Part B"

    status=fields.Selection([('draft', 'Draft Appraisal'),('to_emp', 'Send to Employee'),('sent', 'Sent to Manager'),('to_approve', 'Sent to HR'),('to_md','Sent to MD'),],
            string='Status', store=True,track_visibility='onchange')

    appr_active_kra_rel=fields.Boolean(related='job_requirement_id.appraisal_active',string='Appraisal Active KRA Related',store=True)
    kra_type=fields.Selection([
          ('development', 'Develoment Goals'),
          ('performance', 'Performance Goals'),
          ], string='KRA Type', index=True,track_visibility='onchange')
    kra_1= fields.Text('Job Requirements(KRA)', help="(List each major job requirement and describe the key responsibilities of the function)", track_visibility='onchange')
    kra_description=fields.Text('Description', track_visibility='onchange')
    weightage= fields.Integer('Weightage', track_visibility='onchange')
    emp_rating=fields.Integer('Employee Rating (Rating between 1-5)', help="(Rating should be between 1 and 5)", track_visibility='onchange')
    sop=fields.Text('Standards of Performance (Employee)', help="(Indicate the quality of work that you have exhibited against the Key Roles that are delegated to you)", track_visibility='onchange')
    man_rating=fields.Float('Manager Rating (Rating between 1-5)', help="(Rating should be between 1 and 5)", track_visibility='onchange')
    results= fields.Text('Results Achieved (Manager)', help="(Describe the extent to which the employee has met the standards of performance expected for each major job function.)", track_visibility='onchange')
    job_requirement_id= fields.Many2one('employee.appraisal','Job Requirement Id', track_visibility='onchange')




    @api.one
    @api.constrains('emp_rating')
    def _emp_rating(self):
        record1 = self
        # pattern ="^[1-5]$"
        if record1.emp_rating<=5 and record1.emp_rating>=1 :
            return True
        else:
            raise ValidationError(_('Error: Invalid Rating'))
        return True
    #
    #
    #
    @api.one
    @api.constrains('man_rating')
    def _man_rating(self):
        record2 = self
        # pattern ="^[1-5]$"
        if record2.man_rating<=5 and record2.man_rating>=1:
            return True
        else:
            raise ValidationError(_('Error: Invalid Rating'))
        return True

    # _constraints = [(emp_rating, 'Error: Invalid Rating', ['emp_rating','man_rating']), ]


    @api.one
    @api.constrains('man_rating')
    def _weightage(self, cr, uid, ids, context=None):
        record = self
        if record.weightage != 0:
            return True
        else:
            raise ValidationError(_('Error: Weightage should not be 0'))
        return{}
