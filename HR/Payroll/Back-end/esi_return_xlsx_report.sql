-- Function: public.esi_return_xlsx_report(text)

-- DROP FUNCTION public.esi_return_xlsx_report(text);

CREATE OR REPLACE FUNCTION public.esi_return_xlsx_report(IN month_year text)
  RETURNS TABLE(id integer, ip_number character varying, ip_name character varying, no_of_days integer, wage numeric, employees_contribution numeric, employers_contribution numeric, reason_code integer, last_working_day character varying, date text) AS
$BODY$
DECLARE
   BEGIN

   RETURN query 
 SELECT hpl.id,
    emp.ip_number,
    emp.name AS ip_name,
    0 AS no_of_days,
    hpl.amount AS wage,
    round(hpl.amount * 1.75/100) as Employees_Contribution,
    round(hpl.amount * 4.75/100) as Employers_Contribution,
    hrc.code AS reason_code,
    emp.last_day AS last_working_day,
    to_char(hrp.date_from::timestamp with time zone, 'Mon-YYYY'::text) AS date
   FROM hr_payslip_line hpl,
    hr_employee emp,
    hr_payslip hrp,
    hr_code hrc
  WHERE hpl.code::text = 'GROSS'::text AND hpl.employee_id = emp.id AND hpl.slip_id = hrp.id AND hrc.id= emp.reason_code
  AND to_char(hrp.date_from::timestamp with time zone, 'Mon-YYYY'::text) = month_year
  AND hpl.amount <=21000;
  END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION public.esi_return_xlsx_report(text)
  OWNER TO postgres;
