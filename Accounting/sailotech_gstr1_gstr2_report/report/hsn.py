from odoo import models
import datetime

class GstrHSNXlsx(models.AbstractModel):
    _name = 'report.gst.hsn'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('HSN')
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

        worksheet.write('A%s' %(row), 'HSN')
        worksheet.write('B%s' %(row), 'Description')
        worksheet.write('C%s' %(row), 'UQC')
        worksheet.write('D%s' %(row), 'Total Quantity')
        worksheet.write('E%s' %(row), 'Total Value')
        worksheet.write('F%s' %(row), 'Taxable Value')
        worksheet.write('G%s' %(row), 'Integrated Tax Amount')
        worksheet.write('H%s' %(row), 'Central Tax Amount')
        worksheet.write('I%s' %(row), 'State/UT Tax Amount')
        worksheet.write('J%s' %(row), 'Cess Amount')

        partner_state = self.env.user.company_id.partner_id.state_id.name

        ls = []
        t = []
        for obj in invoice_id:
            for rec in obj.invoice_line_ids:
                ls.append(rec.product_id.l10n_in_hsn_code)

        l10n_in_hsn_code = set(ls)
        for hsn in l10n_in_hsn_code:
            qty = 0
            taxable = 0
            cgst = 0
            sgst = 0
            igst = 0
            uom=''

            for inv in invoice_id:
                for line in inv.invoice_line_ids:
                    if line.product_id.l10n_in_hsn_code == hsn:
                        qty+=line.quantity
                        name = line.name
                        uom = line.uom_id.name
                        if line.invoice_line_tax_ids:
                            for rec in line.invoice_line_tax_ids:
                                if 'GST' in rec.name:
                                    taxable+=line.price_subtotal
                                    if rec.children_tax_ids:
                                        cgst+=(((sum(rec.children_tax_ids.mapped('amount'))/100)*line.price_subtotal)/2)
                                        sgst+=(((sum(rec.children_tax_ids.mapped('amount'))/100)*line.price_subtotal)/2)
                                if 'IGST' in rec.name:
                                    igst+=((rec.amount/100)*line.price_subtotal)

            t_value = taxable+cgst+sgst+igst
            worksheet.write('A%s' %(new_row), hsn)
            worksheet.write('B%s' %(new_row), name)
            worksheet.write('C%s' %(new_row), uom)
            worksheet.write('D%s' %(new_row), qty)
            worksheet.write('E%s' %(new_row), t_value)
            worksheet.write('F%s' %(new_row), taxable)
            worksheet.write('G%s' %(new_row), igst)
            worksheet.write('H%s' %(new_row), cgst)
            worksheet.write('I%s' %(new_row), sgst)
            worksheet.write('J%s' %(new_row), '')

            new_row+=1                       
