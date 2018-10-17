from odoo import api,fields, models


class ConfigSettingspayroll(models.TransientModel):
    _inherit = 'res.config.settings'

    standard_deduction = fields.Integer(string = 'Standard Deduction', store = True)
    national_pension_scheme = fields.Float(string = 'NPS(%)')
    education_cess = fields.Float(string = 'Education Cess(%)')
    sur_charge = fields.Float(string = 'Sur Charge(%)',store = True)
    flexible_pay  = fields.Float(string = 'Flexible Pay(%)')
    employee_pf = fields.Float(string ='Employee PF(%)')
    employers_pf = fields.Float(string = 'Employers PF(%)')
    employee_esi = fields.Float(string = 'Employee ESI(%)')
    employers_esi = fields.Float(string = 'Employers ESI(%)')
    esi_limit = fields.Float(string = 'ESI Limit')
    log_enable = fields.Boolean(string = 'Enable Log')
    hra_reduces_basic_salary_percentage = fields.Float(string = 'Actual Rent Paid-X(%) of Basic Salary')
    permanent_disability_thershold = fields.Float(string = 'Permanent Disability Thershold(%)')
    disability_less_than_thershold = fields.Integer(string = 'DLET', help = "Disability less than thershold")
    disability_greater_than_thershold = fields.Integer(string = 'DGT', help = "Disbility greater than thershold")
    donations_for_funds_charities_factor = fields.Float(string = 'Donations For Funds & Charities Factor(%)')
   
    @api.model
    def get_values(self):
        res = super(ConfigSettingspayroll, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            standard_deduction=int(params.get_param('tax_deduction_type.standard_deduction', default=False)) or False,
            national_pension_scheme=float(params.get_param('tax_deduction_type.national_pension_scheme', default=False)) or False,
            education_cess=float(params.get_param('tax_deduction_type.education_cess', default=False)) or False,
            sur_charge=float(params.get_param('tax_deduction_type.sur_charge', default=False)) or False,
            flexible_pay = float(params.get_param('tax_deduction_type.flexible_pay', default=False)) or False,
            employee_pf = float(params.get_param('tax_deduction_type.employee_pf', default=False)) or False,
            employers_pf = float(params.get_param('tax_deduction_type.employers_pf', default=False)) or False,
            employee_esi = float(params.get_param('tax_deduction_type.employee_esi', default=False)) or False,
            employers_esi = float(params.get_param('tax_deduction_type.employers_esi', default=False)) or False,
            esi_limit = float(params.get_param('tax_deduction_type.esi_limit', default=False)) or False,
            log_enable = bool(params.get_param('tax_deduction_type.log_enable', default=False)) or False,
            hra_reduces_basic_salary_percentage = float(params.get_param('tax_deduction_type.hra_reduces_basic_salary_percentage', default=False)) or False,
            permanent_disability_thershold = float(params.get_param('tax_deduction_type.permanent_disability_thershold', default=False)) or False,
            disability_less_than_thershold = int(params.get_param('tax_deduction_type.disability_less_than_thershold', default=False)) or False,
            disability_greater_than_thershold = int(params.get_param('tax_deduction_type.disability_greater_than_thershold', default=False)) or False,
            donations_for_funds_charities_factor = float(params.get_param('tax_deduction_type.donations_for_funds_charities_factor', default=False)) or False,
                    )
        return res

    @api.multi
    def set_values(self):
        super(ConfigSettingspayroll, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.standard_deduction", self.standard_deduction)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.national_pension_scheme", self.national_pension_scheme)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.education_cess", self.education_cess)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.sur_charge", self.sur_charge)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.flexible_pay", self.flexible_pay)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.employee_pf", self.employee_pf)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.employers_pf", self.employers_pf)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.employee_esi", self.employee_esi)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.employers_esi", self.employers_esi)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.esi_limit", self.esi_limit)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.log_enable", self.log_enable)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.hra_reduces_basic_salary_percentage", self.hra_reduces_basic_salary_percentage)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.permanent_disability_thershold", self.permanent_disability_thershold)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.disability_less_than_thershold", self.disability_less_than_thershold)
        self.env['ir.config_parameter'].sudo().set_param("tax_deduction_type.donations_for_funds_charities_factor", self.donations_for_funds_charities_factor)
        
        




        




