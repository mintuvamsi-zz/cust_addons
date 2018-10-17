-- Function: public.sea_payroll_log_error(integer, text, integer, text)

-- DROP FUNCTION public.sea_payroll_log_error(integer, text, integer, text);

CREATE OR REPLACE FUNCTION public.sea_payroll_log_error(
    p_cid integer,
    p_func_name text,
    p_error_location integer,
    p_error_desc text)
  RETURNS void AS
$BODY$

DECLARE 
		
	BEGIN

			insert into public.sea_payroll_log_error(contract_id,function_name,error_location,error_description) VALUES(p_cid,p_func_name,p_error_location,p_error_desc);
		
		
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_payroll_log_error(integer, text, integer, text)
  OWNER TO odoo;
