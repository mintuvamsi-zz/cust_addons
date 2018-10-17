from odoo import models
import datetime
import psycopg2
import pdb

class GstrB2BXlsx(models.AbstractModel):
    _name = 'report.gst.b2b'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('B2B')
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
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_b2b_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet.write('A%s' %(row), 'GSTIN/UIN of Recipient')
        worksheet.write('B%s' %(row), 'Name')
        worksheet.write('C%s' %(row), 'Number')
        worksheet.write('D%s' %(row), 'Date')
        worksheet.write('E%s' %(row), 'Invoice Value')
        worksheet.write('F%s' %(row), 'Place of Supply')
        worksheet.write('G%s' %(row), 'Reverse Charge')
        worksheet.write('H%s' %(row), 'Invoice Type')
        worksheet.write('I%s' %(row), 'Ecom GSTIN')
        worksheet.write('J%s' %(row), 'Tax Rate')
        worksheet.write('K%s' %(row), 'Price Total')
        worksheet.write('L%s' %(row), 'Cess Amount')

        for i in status:
            new_col+=1
            worksheet.write('A%s' %(new_row), i[0])
            worksheet.write('B%s' %(new_row), i[1])
            worksheet.write('C%s' %(new_row), i[2])
            worksheet.write('D%s' %(new_row), i[3])
            worksheet.write('E%s' %(new_row), i[4])
            worksheet.write('F%s' %(new_row), i[5])
            worksheet.write('G%s' %(new_row), i[6])
            worksheet.write('H%s' %(new_row), i[7])
            worksheet.write('I%s' %(new_row), i[8])
            worksheet.write('J%s' %(new_row), i[9])
            worksheet.write('K%s' %(new_row), i[10])
            worksheet.write('L%s' %(new_row), i[11])
            new_row+=1


# =========================== B2CL================================================================
        worksheet1 = workbook.add_worksheet('B2CL')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet1.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_b2cl_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet1.write('A%s' %(row), 'Invoice Number')
        worksheet1.write('B%s' %(row), 'Invoice Date')
        worksheet1.write('C%s' %(row), 'Invoice Value')
        worksheet1.write('D%s' %(row), 'Place of Supply')
        worksheet1.write('E%s' %(row), 'Tax Rate')
        worksheet1.write('F%s' %(row), 'Price Total')
        worksheet1.write('G%s' %(row), 'Cess Amount')
        worksheet1.write('H%s' %(row), 'Ecom GSTIN')


        for i in status:
            new_col+=1
            worksheet1.write('A%s' %(new_row), i[0])
            worksheet1.write('B%s' %(new_row), i[1])
            worksheet1.write('C%s' %(new_row), i[2])
            worksheet1.write('D%s' %(new_row), i[3])
            worksheet1.write('E%s' %(new_row), i[4])
            worksheet1.write('F%s' %(new_row), i[5])
            worksheet1.write('G%s' %(new_row), i[6])
            worksheet1.write('H%s' %(new_row), i[7])
            new_row+=1

# =========================== B2CS================================================================
        worksheet2 = workbook.add_worksheet('B2CS')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet2.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_b2cs_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet2.write('A%s' %(row), 'Type')
        worksheet2.write('B%s' %(row), 'Place of Supply')
        worksheet2.write('C%s' %(row), 'Tax Rate')
        worksheet2.write('D%s' %(row), 'Price Total')
        worksheet2.write('E%s' %(row), 'Cess Amount')
        worksheet2.write('F%s' %(row), 'Ecom GSTIN')


        for i in status:
            new_col+=1
            worksheet2.write('A%s' %(new_row), i[0])
            worksheet2.write('B%s' %(new_row), i[1])
            worksheet2.write('C%s' %(new_row), i[2])
            worksheet2.write('D%s' %(new_row), i[3])
            worksheet2.write('E%s' %(new_row), i[4])
            worksheet2.write('F%s' %(new_row), i[5])
            new_row+=1
# =========================== CDNR================================================================
        worksheet3 = workbook.add_worksheet('CDNR')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet3.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_cdnr_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet3.write('A%s' %(row), 'GSTIN/UIN of Recipient')
        worksheet3.write('B%s' %(row), 'Name')
        worksheet3.write('C%s' %(row), 'Invoice Number')
        worksheet3.write('D%s' %(row), 'Invoice Date')
        worksheet3.write('E%s' %(row), 'Note Number')
        worksheet3.write('F%s' %(row), 'Note Date')
        worksheet3.write('G%s' %(row), 'Document Type')
        worksheet3.write('H%s' %(row), 'Reason')
        worksheet3.write('I%s' %(row), 'Place of Supply')
        worksheet3.write('J%s' %(row), 'Note Value')
        worksheet3.write('K%s' %(row), 'Tax Rate')
        worksheet3.write('L%s' %(row), 'Taxable Value')
        worksheet3.write('M%s' %(row), 'Cess Amount')
        worksheet3.write('N%s' %(row), 'Pre GST')


        for i in status:
            new_col+=1
            worksheet3.write('A%s' %(new_row), i[0])
            worksheet3.write('B%s' %(new_row), i[1])
            worksheet3.write('C%s' %(new_row), i[2])
            worksheet3.write('D%s' %(new_row), i[3])
            worksheet3.write('E%s' %(new_row), i[4])
            worksheet3.write('F%s' %(new_row), i[5])
            worksheet3.write('G%s' %(new_row), i[6])
            worksheet3.write('H%s' %(new_row), i[7])
            worksheet3.write('I%s' %(new_row), i[8])
            worksheet3.write('J%s' %(new_row), i[9])
            worksheet3.write('K%s' %(new_row), i[10])
            worksheet3.write('L%s' %(new_row), i[11])
            worksheet3.write('M%s' %(new_row), i[12])
            worksheet3.write('N%s' %(new_row), i[13])
            new_row+=1

# =========================== CDNUR================================================================
        worksheet4 = workbook.add_worksheet('CDNUR')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet4.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_cdnur_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet4.write('A%s' %(row), 'UR Type')
        worksheet4.write('B%s' %(row), 'Note Number')
        worksheet4.write('C%s' %(row), 'Note Date')
        worksheet4.write('D%s' %(row), 'Document Type')
        worksheet4.write('E%s' %(row), 'Invoice Number')
        worksheet4.write('F%s' %(row), 'Invoice Date')
        worksheet4.write('G%s' %(row), 'Reason')
        worksheet4.write('H%s' %(row), 'Place of Supply')
        worksheet4.write('I%s' %(row), 'Note Value')
        worksheet4.write('J%s' %(row), 'Tax Rate')
        worksheet4.write('K%s' %(row), 'Taxable Value')
        worksheet4.write('L%s' %(row), 'Cess Amount')
        worksheet4.write('M%s' %(row), 'Pre GST')



        for i in status:
            new_col+=1
            worksheet4.write('A%s' %(new_row), i[0])
            worksheet4.write('B%s' %(new_row), i[1])
            worksheet4.write('C%s' %(new_row), i[2])
            worksheet4.write('D%s' %(new_row), i[3])
            worksheet4.write('E%s' %(new_row), i[4])
            worksheet4.write('F%s' %(new_row), i[5])
            worksheet4.write('G%s' %(new_row), i[6])
            worksheet4.write('H%s' %(new_row), i[7])
            worksheet4.write('I%s' %(new_row), i[8])
            worksheet4.write('J%s' %(new_row), i[9])
            worksheet4.write('K%s' %(new_row), i[10])
            worksheet4.write('L%s' %(new_row), i[11])
            worksheet4.write('M%s' %(new_row), i[12])

            new_row+=1


# =========================== EXP================================================================
        worksheet5 = workbook.add_worksheet('EXP')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet5.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_exp_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet5.write('A%s' %(row), 'Invoice Type')
        worksheet5.write('B%s' %(row), 'Invoice Number')
        worksheet5.write('C%s' %(row), 'Invoice Date')
        worksheet5.write('D%s' %(row), 'Invoice value')
        worksheet5.write('E%s' %(row), 'Port Code')
        worksheet5.write('F%s' %(row), 'Shipping Bill Number')
        worksheet5.write('G%s' %(row), 'Shipping Bill Date')
        worksheet5.write('H%s' %(row), 'Tax Rate')
        worksheet5.write('I%s' %(row), 'Price Subtotal')




        for i in status:
            new_col+=1
            worksheet5.write('A%s' %(new_row), i[0])
            worksheet5.write('B%s' %(new_row), i[1])
            worksheet5.write('C%s' %(new_row), i[2])
            worksheet5.write('D%s' %(new_row), i[3])
            worksheet5.write('E%s' %(new_row), i[4])
            worksheet5.write('F%s' %(new_row), i[5])
            worksheet5.write('G%s' %(new_row), i[6])
            worksheet5.write('H%s' %(new_row), i[7])
            worksheet5.write('I%s' %(new_row), i[8])


            new_row+=1


# =========================== AT ================================================================
        worksheet6 = workbook.add_worksheet('AT')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet6.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_at_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()

        worksheet6.write('A%s' %(row), 'Place of Supply')
        worksheet6.write('B%s' %(row), 'Tax Rate')
        worksheet6.write('C%s' %(row), 'Price Total')
        worksheet6.write('D%s' %(row), 'Cess Amount')




        for i in status:
            new_col+=1
            worksheet6.write('A%s' %(new_row), i[0])
            worksheet6.write('B%s' %(new_row), i[1])
            worksheet6.write('C%s' %(new_row), i[2])
            worksheet6.write('D%s' %(new_row), i[3])

            new_row+=1

# =========================== TXPD ================================================================
        worksheet7 = workbook.add_worksheet('TXPD')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet7.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_txpd_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()

        worksheet7.write('A%s' %(row), 'Place of Supply')
        worksheet7.write('B%s' %(row), 'Tax Rate')
        worksheet7.write('C%s' %(row), 'Price Total')
        worksheet7.write('D%s' %(row), 'Cess Amount')




        for i in status:
            new_col+=1
            worksheet7.write('A%s' %(new_row), i[0])
            worksheet7.write('B%s' %(new_row), i[1])
            worksheet7.write('C%s' %(new_row), i[2])
            worksheet7.write('D%s' %(new_row), i[3])

            new_row+=1



# =========================== HSN ================================================================
        worksheet8 = workbook.add_worksheet('HSN')
        start_date = invoices.start_date
        end_date = invoices.end_date

        invoice_id = self.env['account.invoice'].search([('type','=','out_invoice'),
                                                        ('state', 'in', ['open', 'paid']),
                                                        ('date_invoice','>=',start_date),
                                                        ('date_invoice','<=',end_date)])

        worksheet8.set_column('A:K',15)
        date_format = workbook.add_format({'num_format': 'd-mmm-yyyy'})

        row = 1
        col = 0
        new_row = row + 1
        new_col = col + 1
        y = 'Yes'
        n = 'No'


        self._cr.execute("SELECT * FROM gstr1_export_hsn_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet8.write('A%s' %(row), 'HSN Code')
        worksheet8.write('B%s' %(row), 'Description')
        worksheet8.write('C%s' %(row), 'UQC')
        worksheet8.write('D%s' %(row), 'Quantity')
        worksheet8.write('E%s' %(row), 'Amount Total')
        worksheet8.write('F%s' %(row), 'Price Subtotal')
        worksheet8.write('G%s' %(row), 'IGST')
        worksheet8.write('H%s' %(row), 'CGST')
        worksheet8.write('I%s' %(row), 'SGST')
        worksheet8.write('J%s' %(row), 'Cess Amount')




        for i in status:
            new_col+=1
            worksheet8.write('A%s' %(new_row), i[0])
            worksheet8.write('B%s' %(new_row), i[1])
            worksheet8.write('C%s' %(new_row), i[2])
            worksheet8.write('D%s' %(new_row), i[3])
            worksheet8.write('E%s' %(new_row), i[4])
            worksheet8.write('F%s' %(new_row), i[5])
            worksheet8.write('G%s' %(new_row), i[6])
            worksheet8.write('H%s' %(new_row), i[7])
            worksheet8.write('I%s' %(new_row), i[8])
            worksheet8.write('J%s' %(new_row), i[9])


            new_row+=1
