-- Function: public.pf_ecr_xl_report(text)

-- DROP FUNCTION public.pf_ecr_xl_report(text);

CREATE OR REPLACE FUNCTION public.pf_ecr_xl_report(IN month_year text)
  RETURNS TABLE(month text, uan character varying, name character varying, gross_salary numeric, basic_salary numeric, eps numeric, edli numeric, epf_contribution numeric, eps_contribution numeric, epf_eps_amount_diff numeric, ncp_days integer, refund_of_advances integer) AS
$BODY$
DECLARE
   BEGIN
   RETURN query 
SELECT
    to_char(a.date_from::timestamp with time zone, 'Mon-yyyy'::text) AS month,
    a.uan,
    a.name,
    a.amount AS gross_salary,
    b.wage AS basic_salary,
    b.eps,
    b.edli,
    round(b.wage * 12::numeric / 100::numeric, 0) AS epf_contribution,
    round(b.eps * 8.33 / 100::numeric, 0) AS eps_contribution,
    round(b.wage * 12::numeric / 100::numeric, 0) - round(b.eps * 8.33 / 100::numeric, 0) AS epf_eps_amount_diff,
    0 AS ncp_days,
    0 AS refund_of_advances
   FROM ( SELECT
	    emp.uan,
            emp.name,
            hp.date_from,
            hpl.amount
           FROM hr_employee emp,
            hr_payslip hp,
            hr_payslip_line hpl,
            hr_contract hc
          WHERE hpl.code::text = 'GROSS'::text AND emp.id = hp.employee_id AND hpl.slip_id = hp.id AND hc.employee_id = emp.id
          GROUP BY emp.name, hp.date_from, hpl.amount, hp.id,emp.uan) a,
    ( SELECT 
            emp.name,
            hp.date_from,
            hc.wage,
                CASE
                    WHEN hc.wage > 15000::numeric THEN 15000::numeric
                    ELSE hc.wage
                END AS eps,
                CASE
                    WHEN hc.wage > 15000::numeric THEN 15000::numeric
                    ELSE hc.wage
                END AS edli
           FROM hr_employee emp,
            hr_payslip hp,
            hr_payslip_line hpl,
            hr_contract hc
          WHERE hpl.code::text = 'BASIC'::text AND emp.id = hp.employee_id 
		  AND hpl.slip_id = hp.id AND hc.employee_id = emp.id
          GROUP BY emp.name, hp.date_from, hc.wage, hp.id) b
  WHERE a.name::text = b.name::text AND a.uan is not null
  AND to_char(a.date_from::timestamp with time zone, 'Mon-yyyy'::text)=month_year
  GROUP BY a.name, a.date_from, a.amount, b.wage, b.eps, b.edli,a.uan
  ORDER BY a.date_from;
    END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;