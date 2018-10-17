from odoo import models
from datetime import datetime, date
import re

class GstrExportXlsx(models.AbstractModel):
    _name = 'report.gst.export'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('Export')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1

        worksheet.write('A%s' %(row), 'Export Type')
        worksheet.write('B%s' %(row), 'Invoice Number')
        worksheet.write('C%s' %(row), 'Invoice Date')
        worksheet.write('D%s' %(row), 'Invoice Value')
        worksheet.write('E%s' %(row), 'Port Code')
        worksheet.write('F%s' %(row), 'Shipping Bill No.')
        worksheet.write('G%s' %(row), 'Shipping Bill Date')
        worksheet.write('H%s' %(row), 'Rate')
        worksheet.write('I%s' %(row), 'Taxable Value')

        ls = []
        for obj in invoice_id:
            if obj.export_invoice == True:
                for rec in obj.invoice_line_ids:
                    for line in rec.invoice_line_tax_ids:
                        if line.children_tax_ids:
                            if sum(line.children_tax_ids.mapped('amount')) == 1:
                                ls.append(1)
                            if sum(line.children_tax_ids.mapped('amount')) == 2:
                                ls.append(2)
                            if sum(line.children_tax_ids.mapped('amount')) == 5:
                                ls.append(5)
                            if sum(line.children_tax_ids.mapped('amount')) == 18:
                                ls.append(18)
                            if sum(line.children_tax_ids.mapped('amount')) == 28:
                                ls.append(28)
                        else:
                            if line.amount == 1:
                                ls.append(1)
                            if line.amount == 2:
                                ls.append(2)
                            if line.amount == 5:
                                ls.append(5)
                            if line.amount == 18:
                                ls.append(18)
                            if line.amount == 28:
                                ls.append(28)

        for obj in invoice_id:
            if obj.export_invoice == True:
                for rip in set(ls):
                    r=0
                    for rec in obj.invoice_line_ids:
                        for line in rec.invoice_line_tax_ids:
                            if line.children_tax_ids:
                                if sum(line.children_tax_ids.mapped('amount')) == rip:
                                    r+=rec.price_subtotal
                            else:
                                if line.amount == rip:
                                    r+=rec.price_subtotal

                    if r == 0:
                        pass
                    else:
                        line = re.sub('[-]', '', obj.date_invoice)
                        year = int(line[:4])
                        mon = int(line[4:6])
                        day = int(line[6:8])

                        worksheet.write('A%s' %(new_row), obj.export_type)
                        worksheet.write('B%s' %(new_row), obj.number)
                        worksheet.write('C%s' %(new_row), date(year,mon,day).strftime('%d %b %Y'))
                        worksheet.write('D%s' %(new_row), obj.amount_total)
                        worksheet.write('E%s' %(new_row), obj.port_code.name)
                        worksheet.write('F%s' %(new_row), obj.ship_bill_no)
                        worksheet.write('G%s' %(new_row), obj.ship_bill_date)
                        worksheet.write('H%s' %(new_row), rip)
                        worksheet.write('I%s' %(new_row), r)

                        new_row+=1
