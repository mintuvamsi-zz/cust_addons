from odoo import models
import datetime

class GstrB2CSXlsx(models.AbstractModel):
    _name = 'report.gst.b2cs'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('B2CS')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet.set_column('A:H',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1

        worksheet.write('A%s' %(row), 'Type')
        worksheet.write('B%s' %(row), 'Place Of Supply')
        worksheet.write('C%s' %(row), 'Rate')
        worksheet.write('D%s' %(row), 'Taxable Value')
        worksheet.write('E%s' %(row), 'Cess Amount')
        worksheet.write('F%s' %(row), 'E-Commerce GSTIN')

        ls = []
        for obj in invoice_id:
            if obj.partner_id.vat == False and ((obj.amount_total <= 250000)): #and obj.partner_id.property_account_position_id.name == 'Inter State') or obj.partner_id.property_account_position_id.name == 'Intra State'):
                for rec in obj.invoice_line_ids:
                    if rec.invoice_line_tax_ids:
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



        for rip in set(ls):
            r=0
            for obj in invoice_id:
                if obj.partner_id.vat == False and ((obj.amount_total <= 250000)): #and obj.partner_id.property_account_position_id.name == 'Inter State') or obj.partner_id.property_account_position_id.name == 'Intra State'):
                    for rec in obj.invoice_line_ids:
                        if rec.invoice_line_tax_ids:
                            for line in rec.invoice_line_tax_ids:
                                if line.children_tax_ids:
                                    if sum(line.children_tax_ids.mapped('amount')) == rip:
                                        r+=rec.price_subtotal
                                else:
                                    if line.amount == rip:
                                        r+=rec.price_subtotal

            worksheet.write('A%s' %(new_row), 'OE')
            worksheet.write_rich_string('B%s' %(new_row), str(obj.partner_id.state_id.state_code) + str("-") + str(obj.partner_id.state_id.name))
            worksheet.write('C%s' %(new_row), rip)
            worksheet.write('D%s' %(new_row), r)
            worksheet.write('E%s' %(new_row), '')
            worksheet.write('F%s' %(new_row), '')

            new_row+=1
