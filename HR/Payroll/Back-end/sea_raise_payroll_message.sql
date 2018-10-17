-- Function: public.sea_raise_payroll_message(character varying, integer, integer, date)

-- DROP FUNCTION public.sea_raise_payroll_message(character varying, integer, integer, date);

CREATE OR REPLACE FUNCTION public.sea_raise_payroll_message(
    p_msg_code character varying,
    p_cid integer,
    p_emp_name integer,
    p_payroll_month date)
  RETURNS void AS
$BODY$

DECLARE 
		error_desc TEXT;
		cnt integer;
	BEGIN
			
			INSERT INTO public.sea_payroll_messages (contract_id, emp_name, payroll_month, message)
			SELECT p_cid,p_emp_name,p_payroll_month,message
			FROM
				public.sea_messages_master
			WHERE
				msg_code = p_msg_code;
				
			GET DIAGNOSTICS cnt = ROW_COUNT;
			IF cnt=0 
			THEN
				RAISE NOTICE 'Message code % does not exist.Please contact administrator',p_msg_code;
			END IF;
		--RETURN 'Message '||p_msg_code||' inserted successfully';
	exception
         WHEN others THEN
            RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;
        --RETURN 'Message '||p_msg_code|| ' does not exist.Please contact administrator';

		
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_raise_payroll_message(character varying, integer, integer, date)
  OWNER TO odoo;
