-- Function: public.payment_advice_xlsx_report(character varying)

-- DROP FUNCTION public.payment_advice_xlsx_report(character varying);

CREATE OR REPLACE FUNCTION public.payment_advice_xlsx_report(IN p_reference character varying)
  RETURNS TABLE(payment_advice character varying, date date, bank_name character varying, employee_name character varying, account_number character varying, ifsc_code character varying, salary numeric, debit_credit character varying) AS
$BODY$
BEGIN

RETURN query

select hpa.name as payment_advice ,hpa.date as date,rb.name as bank_name,he.name as employee_name,
       hpal.name as account_number,hpal.ifsc_code as ifsc_code,hpal.bysal as salary,hpal.debit_credit as debit_credit 
from hr_payroll_advice hpa,hr_payroll_advice_line hpal,res_partner_bank rpb,hr_employee he,res_bank rb
where hpa.id = hpal.advice_id  and rb.id = hpa.bank_id and hpal.employee_id = he.id and hpal.name = rpb.acc_number and hpa.number = p_reference
order by 1 desc;

END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.payment_advice_xlsx_report(character varying)
  OWNER TO postgres;
