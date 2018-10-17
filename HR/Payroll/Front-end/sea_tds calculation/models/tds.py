from odoo import api, fields, models, tools, SUPERUSER_ID, _
import psycopg2
import base64
import hashlib
import pytz
import threading
from odoo.addons import decimal_precision as dp

from email.utils import formataddr

from werkzeug import urls

from odoo.modules import get_module_resource

class HrContractTds(models.Model):

    _inherit = 'hr.contract'

    tds_cal = fields.Char('Calculate Tds')
    exemptions_undersection = fields.Integer(string = 'Exemption Under Section 10&17',readonly = 'True')
    income_chargeable_houseproperty = fields.Integer(string = 'Income chargeable under head House/Property',readonly = 'True') 
    income_chargeable_otherhead_sources = fields.Integer(string = 'Income chargeable under head Other Sources',readonly = 'True') 
    deductions_underchapter_6a = fields.Integer(string = 'Deductions under chapter VI-A',readonly = 'True')
    deductions_under80c_80ccd = fields.Integer(string = 'Deductions Under Section 80C & 80CCD',readonly = 'True')
    cost_to_company = fields.Float(string ='Cost To Company', required=True)
    special_allowance = fields.Float(string = 'Special Allowance')
    employee_pf = fields.Float(string = 'Employee PF')
    employeepf_exempt = fields.Boolean(string = 'Provision')
    employers_pf = fields.Float(string = 'Employers PF')
    employerspf_exempt = fields.Boolean(string = 'Provision')
    gratuity = fields.Float(string = 'Gratuity')
    gratuity_exempt = fields.Boolean('Provision')
    petrol_bill = fields.Integer('Petrol Bill')
    petrolbill_exempt = fields.Boolean('Provision')
    lta = fields.Integer('LTA')
    lta_exempt = fields.Boolean('Provision')
    telephone_bill = fields.Integer('Telephone Bill')
    telephonebill_exempt = fields.Boolean('Provision')
    hra_exempt = fields.Boolean('Provision')
    conveyance_allowance = fields.Integer('Conveyance Allowance')
    conveyanceallowance_exempt = fields.Boolean('Provision')
    flexible_pay = fields.Integer(string = 'Flexible Allowance')
    flexiblepay_exempt = fields.Boolean('Provision')
    medicalinsurance_exempt = fields.Boolean('Provision')
    employee_esi = fields.Float(string = 'Employee ESI')
    employeeesi_exempt = fields.Boolean(string = 'Provision')
    employers_esi = fields.Float(string = 'Employers ESI')
    employersesi_exempt = fields.Boolean(string = 'Provision')
    meal_vouchers = fields.Float(string = 'Meal Vouchers')
    mealvouchers_exempt = fields.Boolean(string ='Provision')
    insurance = fields.Float(string = 'Insurance')
    insurance_exempt = fields.Boolean(string = 'Provision')
    nontaxable_reimbursment = fields.Integer(string = 'Non Taxable Reimbursment')
    gross_salary = fields.Float(string = 'Gross Salary')
    driver_salary = fields.Float(string = 'Driver Salary')
    driver_salary_exempt = fields.Boolean(string = 'Provision')
    professional_tax = fields.Integer(string = 'Professional Tax')
    # professional_tax_exempt = fields.Boolean(string = 'Provision')
    wage = fields.Monetary('Basic Salary', digits=(16, 2), required=True, help="Employee's monthly basic salary.")
    # hra_recieved = fields.Float(string = 'Annual HRA Received')
    project = fields.Float(string = 'Project')
    incentives = fields.Float(string = 'Incentives')
    # bonus = fields.Float(string = 'Bonus')
    net_taxable_income = fields.Float(string = 'Net Taxable Income')
    basic_salary_percentage = fields.Selection([('30','30%'),('40','40%'),('50','50%')],  string='Basic Salary(%)')
    income_received_previous_employee = fields.Float(string = 'Income Received From Previous Employee')
    previous_professional_tax = fields.Float(string = 'Previous Professional Tax')
    previous_employer_tds = fields.Float(string = 'Previous Employer TDS')
    # hra_exemption = fields.Float(string = 'HRA Exemption')
    # annual_tds_with_sur_cess_charges = fields.Float(string = 'Annual TDS')
    # tds_upto_current_month_with_sur_cess_charges = fields.Float(string = 'TDS Deducted So Far')
    # balance_tds_recovered_with_charges = fields.Float(string = 'TDS To Be Deducted')
    # avg_bal_tds_with_charges = fields.Float(string = 'Average TDS Balance With Charges')
    # deductions_under80c = fields.Integer(string = 'Deductions under section 80C')
    standard_deduction = fields.Integer(string = 'Standard Deduction')
    # providentfund_80c = fields.Integer(string = 'provident fund under 80C')
    # housing_loan_principal_amount_80C = fields.Integer(string = 'Housing Loan Principal Amount Under 80C')
    # surcharge_on_income_tax = fields.Integer(string = 'surcharge')
    # education_cess = fields.Integer(string = 'Cess')
    # actualhra_reduces_basic = fields.Integer(string = 'actual rent paid')
    # hra_40percent = fields.Integer(string = '40 of basic salary')
    # house_property_income_loss = fields.Integer(string = 'House Property Income/Loss')
    leave_details = fields.Text(string = 'Leave Details')
    any_other_deductions = fields.Integer(string ='Additional Deductions')
    shift_allowance = fields.Float(string = 'Shift Allowance')
    tds = fields.Float(string='Monthly TDS To Be Deducted', digits=dp.get_precision('Payroll'),
        help='Amount for Tax Deduction at Source')







    @api.multi
    def tds_cal_auto(self):
        p_id=str(self.id)
        self._cr.execute( "select * from sea_calculate_tds('"+p_id +"')")
        # pdb.set_trace()
        self.tds_cal = self._cr.fetchone()[0]

        
    @api.multi
    def calculate_cashcomponents(self):
        p_cid=str(self.id)
        self._cr.execute( "select * from sea_payroll_calculate_components('"+p_cid +"')")
        # pdb.set_trace()
        # self.special_allowance = self._cr.fetchone()[0]