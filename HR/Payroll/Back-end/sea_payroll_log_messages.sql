-- Function: public.sea_payroll_log_messages(integer, integer, character varying, character varying, character varying)

-- DROP FUNCTION public.sea_payroll_log_messages(integer, integer, character varying, character varying, character varying);

CREATE OR REPLACE FUNCTION public.sea_payroll_log_messages(
    p_cid integer,
    p_loc integer,
    p_func_name character varying,
    p_msg_desc character varying,
    p_msg_value character varying)
  RETURNS void AS
$BODY$

DECLARE 
		l_log_flag BOOLEAN;
		l_loction numeric :=0;
	BEGIN
	l_loction := 10;
		BEGIN
			l_loction := 20;
			select log_enable into l_log_flag from public.res_config_settings order by id desc limit 1;
			IF NOT FOUND 
			THEN
				l_log_flag:=FALSE;
			END IF;
		exception
				WHEN OTHERS THEN
				RAISE INFO 'Error Name:%', SQLERRM;
				RAISE INFO 'Error State:%', SQLSTATE;	
			--PERFORM public.sea_payroll_log_error(p_cid,'sea_payroll_log_messages'::text,l_loction,SQLSTATE||' : '||SQLERRM);
			
			
		END;
		
		IF l_log_flag IS FALSE
		THEN
			l_loction := 30;
			insert into public.sea_log_messages(contract_id,function_name,message_desc,message_value,location) VALUES(p_cid,p_func_name,p_msg_desc,p_msg_value,p_loc);
		
		END IF;
		
	exception
		WHEN OTHERS THEN
		RAISE INFO 'Error Name:%', SQLERRM;
		RAISE INFO 'Error State:%', SQLSTATE;	
		--PERFORM public.sea_payroll_log_error(p_cid,'sea_payroll_log_messages'::text,l_loction,SQLSTATE||' : '||SQLERRM);
			
		
		
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_payroll_log_messages(integer, integer, character varying, character varying, character varying)
  OWNER TO odoo;
