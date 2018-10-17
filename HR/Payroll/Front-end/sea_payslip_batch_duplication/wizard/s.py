import time
from datetime import datetime, timedelta
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class hrpayslipbatchwizard(models.TransientModel):
	#_inherit = 'hr.payslip.run'

	_name = 'hr.payslip.batch.wizard'

	p_name = fields.Many2one('hr.payslip.run','Name')
	#name = fields.Char('Name')
	date_from = fields.Date(string='Date From')
	date_to = fields.Date(string='Date To')
	
	@api.multi
	def duplicate_batch(self):
		in_name=str(self.p_name)
		in_fromdt=str(self.date_from)
		in_todt=str(self.date_to)
		self._cr.execute("select insert_same_data_with_batch_b('"+str(in_name)+"','"+in_fromdt+"','"+in_todt+"')")
# 		self.name=self._cr.fetchone()[0]
# 		self.date_start =self._cr.fetchone()[0]
# 		self.date_end =self._cr.fetchone()[0]

# #payslip
	
# 		self._cr.execute("""SELECT struct_id,
# 						name,
# 						number,
# 						employee_id,
# 						date_from,
# 						date_to,
# 						state,
# 						company_id,
# 						paid,
# 						note,
# 						contract_id,
# 						credit_note,
# 						payslip_run_id	
# 					FROM hr_payslip WHERE payslip_run_id = p_name;

# 			#self._cr.fetchall():
# 						# struct_id,
# 						# name,
# 						# number,
# 						# employee_id,
# 	 			 #    	in_fromdt,
# 						# in_todt,
# 						# state,
# 		 			# 	company_id,
# 						# paid,
# 		 			# 	note,
# 						# contract_id,
# 						# credit_note, payslip_run_id = row

# 					INSERT INTO hr_payslip
# 		               (struct_id,
# 						name,
# 						number,
# 						employee_id,
# 						in_fromdt,
# 						in_todt,
# 						state,
# 						company_id,
# 						paid,
# 						note,
# 						contract_id,
# 						credit_note,
# 						p_name) 
# 						VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" %
# 						(struct_id,
# 						name,
# 						number,
# 						employee_id,
# 						in_fromdt,
# 						in_todt,
# 						state,
# 						company_id,
# 						paid,
# 						note,
# 						contract_id,
# 						credit_note,
# 						p_name) )

		# self._cr.fetchall():
		# 				struct_id,
		# 				name,
		# 				number,
		# 				employee_id,
		# 				in_fromdt,
		# 				in_todt,
		# 				state,
		# 				company_id,
		# 				paid,
		# 				note,
		# 				contract_id,
		# 				credit_note,
		# 				payslip_run_id = row
		
		# self._cr.execute("""INSERT INTO hr_payslip
		#                (struct_id,
		# 				name,
		# 				number,
		# 				employee_id,
		# 				in_fromdt,
		# 				in_todt,
		# 				state,
		# 				company_id,
		# 				paid,
		# 				note,
		# 				contract_id,
		# 				credit_note,
		# 				payslip_run_id) 
		# 				VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
		# 				(struct_id,
		# 				name,
		# 				number,
		# 				employee_id,
		# 				in_fromdt,
		# 				in_todt,
		# 				state,
		# 				company_id,
		# 				paid,
		# 				note,
		# 				contract_id,
		# 				credit_note,
		# 				payslip_run_id) )



 #     cursor.execute('SELECT CONCAT(Att_Date," ",in_time) as in_time , CONCAT(Att_Date," ",out_time) as out_time FROM attendance_report.attendance_report_new;')
 #      for row in cursor.fetchall():
 #          check_in, check_out = row
 #      self._cr.execute("insert into biometric_attendance(check_in,check_out) values(%s,%s) " , (check_in,check_out) )

 # 