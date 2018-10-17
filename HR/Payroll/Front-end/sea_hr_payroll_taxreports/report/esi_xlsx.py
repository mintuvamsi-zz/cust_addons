from odoo import models
import datetime
import psycopg2
import pdb

class PF_ESI_Xlsx(models.AbstractModel):
    _name = 'report.esi.return'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('PF ESI')
        # start_date = invoices.start_date
        # end_date = invoices.end_date
        month_year=invoices.month_year


        # invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
        #                                                 ('state', 'in', ['open', 'paid']),
        #                                                 ('date_invoice','>=',start_date),
        #                                                 ('date_invoice','<=',end_date)])

        #id=self.env['pf.ecr'].search([('date','=',month_year)])

        worksheet.set_column('A:J',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'

#        self._cr.execute("SELECT name, gross_salary, basic_salary, eps, edli, epf_contribution, eps_contribution, epf_eps_amount_diff, ncp_days, refund_of_advances FROM pf_ecr_xl_report('"+str(month_year)+"')")
        self._cr.execute("SELECT ip_number, ip_name, no_of_days, wage, Employees_Contribution, Employers_Contribution, reason_code, last_working_day FROM esi_return_xlsx_report('"+str(month_year)+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        # worksheet.write('A%s' %(row), 'Month of year')
        worksheet.write('A%s' %(row), 'IP Number')
        worksheet.write('B%s' %(row), 'IP Name')
        worksheet.write('C%s' %(row), 'No of Days')
        worksheet.write('D%s' %(row), 'Total Monthly Wages')
        worksheet.write('E%s' %(row), 'Employees Contribution')
        worksheet.write('F%s' %(row), 'Employers Contribution')
        worksheet.write('G%s' %(row), 'Reason Code')
        worksheet.write('H%s' %(row), 'Last Working Day')

        for i in status:
            new_col+=1
            # worksheet.write('A%s' %(new_row), i[0])
            worksheet.write('A%s' %(new_row), i[0])
            worksheet.write('B%s' %(new_row), i[1])
            worksheet.write('C%s' %(new_row), i[2])
            worksheet.write('D%s' %(new_row), i[3])
            worksheet.write('E%s' %(new_row), i[4])
            worksheet.write('F%s' %(new_row), i[5])
            worksheet.write('G%s' %(new_row), i[6])
            worksheet.write('H%s' %(new_row), i[7])
            new_row+=1
