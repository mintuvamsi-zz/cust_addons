-- Function: public.sea_tax_exemption_section(integer, integer, text)

-- DROP FUNCTION public.sea_tax_exemption_section(integer, integer, text);

CREATE OR REPLACE FUNCTION public.sea_tax_exemption_section(
    p_cid integer,
    p_emp_id integer,
    p_section_type text)
  RETURNS text AS
$BODY$
	
DECLARE 
	l_return_exemption_value numeric :=0 ;
	l_loction integer := 0;
	BEGIN
		l_loction := 10;
		select sum(allowed_limit) into  l_return_exemption_value
		from employee_taxlines etl,
		employee_taxdeduction_header eth
		where etl.employee_sectionlines=eth.id 
		and eth.employee_id=p_emp_id
		and etl.section_id=p_section_type;
		IF NOT FOUND 
		THEN 
			l_return_exemption_value := 0;
			
		END IF;
		l_loction := 20;
		RETURN coalesce(l_return_exemption_value,0);
		
	exception
		WHEN OTHERS THEN
		RAISE INFO 'Error Name:%', SQLERRM;
		RAISE INFO 'Error State:%', SQLSTATE;	
		PERFORM public.sea_payroll_log_error(p_cid,'sea_tax_exemption_section',l_loction,SQLSTATE||' : '||SQLERRM);
		RETURN 'Error '||SQLSTATE||' : '||SQLERRM;
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_tax_exemption_section(integer, integer, text)
  OWNER TO odoo;
