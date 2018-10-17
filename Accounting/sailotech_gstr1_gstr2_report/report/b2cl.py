from odoo import models
import datetime
import psycopg2
import pdb

class GstrB2CLXlsx(models.AbstractModel):
    _name = 'report.gst.b2cl'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoices):

        worksheet = workbook.add_worksheet('B2CL')
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
        new_col = col + 1
        y = 'Yes'
        n = 'No'



        self._cr.execute("SELECT * FROM gstr2_export_b2b_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet.write('A%s' %(row), 'GSTIN Supplier')
        worksheet.write('B%s' %(row), 'Invoice Number')
        worksheet.write('C%s' %(row), 'Invoice Date')
        worksheet.write('D%s' %(row), 'Invoice Value')
        worksheet.write('E%s' %(row), 'Place of Supply')
        worksheet.write('F%s' %(row), 'Reverse Charge')
        worksheet.write('G%s' %(row), 'Invoice Type')
        worksheet.write('H%s' %(row), 'Rate')
        worksheet.write('I%s' %(row), 'Taxable value')
        worksheet.write('J%s' %(row), 'Integrated Tax Paid')
        worksheet.write('K%s' %(row), 'Central Tax Paid')
        worksheet.write('L%s' %(row), 'State UT Tax Paid')
        worksheet.write('M%s' %(row), 'Cess Paid')
        worksheet.write('N%s' %(row), 'Eligibility Type')
        worksheet.write('O%s' %(row), 'Availed IT Integrated Tax')
        worksheet.write('P%s' %(row), 'Availed IT Central Tax')
        worksheet.write('Q%s' %(row), 'Availed IT State UT Tax')
        worksheet.write('R%s' %(row), 'Availed IT Cess')


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
            worksheet.write('M%s' %(new_row), i[12])
            worksheet.write('N%s' %(new_row), i[13])
            worksheet.write('O%s' %(new_row), i[14])
            worksheet.write('P%s' %(new_row), i[15])
            worksheet.write('Q%s' %(new_row), i[16])
            worksheet.write('R%s' %(new_row), i[17])
            new_row+=1


# =========================== B2BUR ================================================================
        worksheet1 = workbook.add_worksheet('B2BUR')
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


        self._cr.execute("SELECT * FROM gstr2_export_b2bur_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet1.write('A%s' %(row), 'Supplier Name')
        worksheet1.write('B%s' %(row), 'Invoice Number')
        worksheet1.write('C%s' %(row), 'Invoice Date')
        worksheet1.write('D%s' %(row), 'Invoice Value')
        worksheet1.write('E%s' %(row), 'Place of Supply')
        worksheet1.write('F%s' %(row), 'Supply Type')
        worksheet1.write('G%s' %(row), 'Tax Rate')
        worksheet1.write('H%s' %(row), 'Taxable Value')
        worksheet1.write('I%s' %(row), 'Integrated Tax Paid')
        worksheet1.write('J%s' %(row), 'Central Tax Paid')
        worksheet1.write('K%s' %(row), 'State UT Tax Paid')
        worksheet1.write('L%s' %(row), 'Cess Paid')
        worksheet1.write('M%s' %(row), 'Eligibility Type')
        worksheet1.write('N%s' %(row), 'Availed IT Integrated Tax')
        worksheet1.write('O%s' %(row), 'Availed IT Central Tax')
        worksheet1.write('P%s' %(row), 'Availed IT State UT Tax')
        worksheet1.write('Q%s' %(row), 'Availed IT Cess')


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
            worksheet1.write('I%s' %(new_row), i[8])
            worksheet1.write('J%s' %(new_row), i[9])
            worksheet1.write('K%s' %(new_row), i[10])
            worksheet1.write('L%s' %(new_row), i[11])
            worksheet1.write('M%s' %(new_row), i[12])
            worksheet1.write('N%s' %(new_row), i[13])
            worksheet1.write('O%s' %(new_row), i[14])
            worksheet1.write('P%s' %(new_row), i[15])
            worksheet1.write('Q%s' %(new_row), i[16])
            new_row+=1


# =========================== IMPG ================================================================
        worksheet2 = workbook.add_worksheet('IMPG')
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


        self._cr.execute("SELECT * FROM gstr2_export_impg_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet2.write('A%s' %(row), 'Port Code')
        worksheet2.write('B%s' %(row), 'Bill of Entry')
        worksheet2.write('C%s' %(row), 'Date Invoice')
        worksheet2.write('D%s' %(row), 'Amount Total')
        worksheet2.write('E%s' %(row), 'Doc Type')
        worksheet2.write('F%s' %(row), 'GSTIN of SEZ')
        worksheet2.write('G%s' %(row), 'Rate')
        worksheet2.write('H%s' %(row), 'Price Subtotal')
        worksheet2.write('I%s' %(row), 'Tax Amount')
        worksheet2.write('J%s' %(row), 'Cess Paid Amount')
        worksheet2.write('K%s' %(row), 'Eligibility Type')
        worksheet2.write('L%s' %(row), 'ITC Tax')
        worksheet2.write('M%s' %(row), 'ITC Cess Amount')


        for i in status:
            new_col+=1
            worksheet2.write('A%s' %(new_row), i[0])
            worksheet2.write('B%s' %(new_row), i[1])
            worksheet2.write('C%s' %(new_row), i[2])
            worksheet2.write('D%s' %(new_row), i[3])
            worksheet2.write('E%s' %(new_row), i[4])
            worksheet2.write('F%s' %(new_row), i[5])
            worksheet2.write('G%s' %(new_row), i[6])
            worksheet2.write('H%s' %(new_row), i[7])
            worksheet2.write('I%s' %(new_row), i[8])
            worksheet2.write('J%s' %(new_row), i[9])
            worksheet2.write('K%s' %(new_row), i[10])
            worksheet2.write('L%s' %(new_row), i[11])
            worksheet2.write('M%s' %(new_row), i[12])
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


        self._cr.execute("SELECT * FROM gstr2_export_cdnur_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet4.write('A%s' %(row), 'Voucher Number')
        worksheet4.write('B%s' %(row), 'Voucher Date')
        worksheet4.write('C%s' %(row), 'Invoice Number')
        worksheet4.write('D%s' %(row), 'Invoice Date')
        worksheet4.write('E%s' %(row), 'Pre GST')
        worksheet4.write('F%s' %(row), 'Document Type')
        worksheet4.write('G%s' %(row), 'Reason')
        worksheet4.write('H%s' %(row), 'Supply Type')
        worksheet4.write('I%s' %(row), 'Note Value')
        worksheet4.write('J%s' %(row), 'Tax Rate')
        worksheet4.write('K%s' %(row), 'Taxable Value')
        worksheet4.write('L%s' %(row), 'Integrated Tax Paid')
        worksheet4.write('M%s' %(row), 'Central Tax Paid')
        worksheet4.write('N%s' %(row), 'State UT Tax Paid')
        worksheet4.write('O%s' %(row), 'Cess Paid')
        worksheet4.write('P%s' %(row), 'Eligibility Type')
        worksheet4.write('Q%s' %(row), 'Availed IT Integrated Tax')
        worksheet4.write('R%s' %(row), 'Availed IT Central Tax')
        worksheet4.write('S%s' %(row), 'Availed IT State UT Tax')
        worksheet4.write('T%s' %(row), 'Availed IT Cess')



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
            worksheet4.write('N%s' %(new_row), i[13])
            worksheet4.write('O%s' %(new_row), i[14])
            worksheet4.write('P%s' %(new_row), i[15])
            worksheet4.write('Q%s' %(new_row), i[16])
            worksheet4.write('R%s' %(new_row), i[17])
            worksheet4.write('S%s' %(new_row), i[18])
            worksheet4.write('T%s' %(new_row), i[19])


            new_row+=1


# =========================== IMPS ================================================================
        worksheet5 = workbook.add_worksheet('IMPS')
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


        self._cr.execute("SELECT * FROM gstr2_export_impg_v('"+start_date+"', '"+end_date+"')")
        status=self._cr.fetchall()
        #pdb.set_trace()
        worksheet5.write('A%s' %(row), 'Invoice ID')
        worksheet5.write('B%s' %(row), 'Invoice Date')
        worksheet5.write('C%s' %(row), 'Amount Total')
        worksheet5.write('D%s' %(row), 'Place of Supply')
        worksheet5.write('E%s' %(row), 'Rate')
        worksheet5.write('F%s' %(row), 'Price Subtotal')
        worksheet5.write('G%s' %(row), 'Tax Amount')
        worksheet5.write('H%s' %(row), 'Cess Paid Amount')
        worksheet5.write('I%s' %(row), 'Eligibility Type')
        worksheet5.write('J%s' %(row), 'ITC Cess Amount')



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
            worksheet5.write('J%s' %(new_row), i[9])

            new_row+=1


# =========================== TXPD================================================================
        worksheet6 = workbook.add_worksheet('TXPD')
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


        self._cr.execute("SELECT * FROM gstr2_export_txpd_v('"+start_date+"', '"+end_date+"')")
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



# =========================== AT ================================================================
        worksheet7 = workbook.add_worksheet('AT')
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


        self._cr.execute("SELECT * FROM gstr2_export_at_v('"+start_date+"', '"+end_date+"')")
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


        self._cr.execute("SELECT * FROM gstr2_export_hsn_v('"+start_date+"', '"+end_date+"')")
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
