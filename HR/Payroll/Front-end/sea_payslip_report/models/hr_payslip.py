from odoo import models, fields, api
from odoo import tools
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero
import datetime
from dateutil import relativedelta
# from odoo import datetime
# from odoo.tools import amount_to_text_en
# from odoo.tools.amount_to_text import amount_to_text
import pdb


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    annual_tds_with_charges = fields.Float(string = 'Annual TDS')
    providentfund_80c = fields.Integer(string = 'provident fund under 80C')
    housing_loan_principal_amount_80C = fields.Integer(string = 'Housing Loan Principal Amount Under 80C')
    surcharge_on_income_tax = fields.Float(string = 'surcharge')
    education_cess = fields.Float(string = 'Cess')
    actualhra_reduces_basic = fields.Integer(string = 'actual rent paid')
    hra_40percent = fields.Integer(string = '40 of basic salary')
    annual_hra_received = fields.Float(string = 'Annual HRA Received')
    hra_exemption = fields.Float(string = 'HRA Exemption')


    
# this function will calculates cumulative,addition,exemption,annual calculation based on the financial year
    @api.multi
    def get_payslip_lines_rec(self):

        # self.hra_exemption = []
        date = datetime.datetime.strptime(self.date_from, "%Y-%m-%d").date()
        year_of_date=date.year
        financial_year_start_date = datetime.datetime.strptime(str(year_of_date)+"-04-01","%Y-%m-%d").date()
        if date<financial_year_start_date:

            fin_start_year =financial_year_start_date.year-1
            fin_end_year=financial_year_start_date.year
            fin_start_date=datetime.datetime.strptime(str(fin_start_year)+"-03-01","%Y-%m-%d").date()
            fin_end_date=datetime.datetime.strptime(str(fin_end_year)+"-03-31","%Y-%m-%d").date()

            payslip_rec = self.env['hr.payslip'].search([('employee_id','=', self.employee_id.id),('date_from','>=',str(fin_start_date)),('date_to','<',str(fin_end_date))])

        else:

            fin_start_year =financial_year_start_date.year
            fin_end_year=financial_year_start_date.year+1
            fin_start_date=datetime.datetime.strptime(str(fin_start_year)+"-04-01","%Y-%m-%d").date()
            fin_end_date=datetime.datetime.strptime(str(fin_end_year)+"-03-31","%Y-%m-%d").date()
            payslip_rec = self.env['hr.payslip'].search([('employee_id','=', self.employee_id.id),('date_from','>=',str(fin_start_date)),('date_to','<=',str(fin_end_date))])
        result={}
        sum_basic=0
        sum_hra=0
        sum_ntar=0
        sum_fp=0
        sum_sfa=0
        sum_pt=0
        sum_tds =0
        # sum_meal =0
        count=0


        
                
        for payslip in payslip_rec:
            for line_work in payslip.worked_days_line_ids:
                if line_work.code == 'WORK100':
                    result['worked_days'] = line_work.number_of_days
                elif line_work.code == 'UNPAID':
                    result['unpaid_days'] = line_work.number_of_days

            sum_lines=[]


            if self.date_from>=payslip.date_from:
                # pdb.set_trace()
                
                count=count+1
                for line in payslip.line_ids:
                    if line.code == 'BASIC':
                        sum_basic = sum_basic + line.amount

                    elif line.code == 'HRAMN':
                        sum_hra = sum_hra + line.amount
                    elif line.code == 'SFA':
                        sum_sfa = sum_sfa + line.amount
                    elif line.code == 'NTAR':
                        sum_ntar = sum_ntar + line.amount
                    elif line.code == 'PTD':
                        sum_pt = sum_pt + line.amount
                    elif line.code == 'TDS':
                        sum_tds = sum_tds + line.amount
                    # elif line.code == 'MA':
                    #     sum_meal = sum_meal + line.amount
        result['comm_sum_basic']=sum_basic
        result['comm_sum_sfa']=sum_sfa
        result['comm_sum_ntar']=sum_ntar
        result['comm_sum_tds']=sum_tds
        result['comm_sum_hra']=sum_hra
        result['comm_sum_pt']=sum_pt
        # result['comm_sum_meal']=sum_meal
        # pdb.set_trace()
        # len_remaining_months=12-count
        
        fin_date=datetime.datetime.strptime(str(fin_end_date),'%Y-%m-%d')
        current_date = datetime.datetime.strptime(str(self.date_to),'%Y-%m-%d')

        r= relativedelta.relativedelta(fin_date,current_date)
        remaining_months=r.months
        if remaining_months==0:
            remaining_months=1

        result['len_remaining_months'] = remaining_months
        # pdb.set_trace()


        for line in self.line_ids:
            if line.code == 'BASIC':
                result['add_sum_basic']=line.amount*remaining_months
            elif line.code == 'HRAMN':
                result['add_sum_hra']=line.amount*remaining_months
            elif line.code == 'SFA':
                result['add_sum_sfa']=line.amount*remaining_months
            elif line.code == 'NTAR':
                result['add_sum_ntar']=line.amount*remaining_months
            elif line.code == 'TDS':
                result['add_sum_tds']=line.amount*remaining_months
            elif line.code == 'PTD':
                result['add_sum_pt']=line.amount*remaining_months
            # elif line.code == 'MA':
            #     result['add_sum_meal']=line.amount*remaining_months


        result['annual_sum_basic']=result['comm_sum_basic']+result['add_sum_basic']
        result['annual_sum_sfa']=result['comm_sum_sfa']+result['add_sum_sfa']
        result['annual_sum_hra']=result['comm_sum_hra']+result['add_sum_hra']
        result['annual_sum_tds']=result['comm_sum_tds']+result['add_sum_tds']
        result['annual_sum_ntar']=result['comm_sum_ntar']+result['add_sum_ntar']
        result['annual_sum_pt']=result['comm_sum_pt']+result['add_sum_pt']
        # result['annual_sum_meal']=result['comm_sum_meal']+result['add_sum_meal']

        # employee_tax_rec = self.env['employee.taxdeduction.header'].search([('employee_id', '=', self.employee_id.id)])
        #  for tax_lines in employee_tax_rec:
        #      for employee_tax_lines in tax_lines.employee_header_id:
        #          if employee_tax_lines.deduction_desc == 'Employees Provident Fund & Voluntary PF (sec 80C)':
        #              result['provident_fund'] = employee_tax_lines.amount
        #          elif employee_tax_lines.deduction_desc == 'Housing loan principal repayment, regn/stamp duty (sec 80C)':
        #              result['housing_loan_principal'] = employee_tax_lines.amount


        return result

       
    









