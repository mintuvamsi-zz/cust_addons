-- Function: public.sea_get_tax_value(integer, numeric)

-- DROP FUNCTION public.sea_get_tax_value(integer, numeric);

CREATE OR REPLACE FUNCTION public.sea_get_tax_value(
    p_cid integer,
    p_gross_value numeric)
  RETURNS text AS
$BODY$

DECLARE 
		l_ret_tx_amount numeric;
		l_loction integer :=0;
	BEGIN
		l_loction :=10;
		DROP TABLE IF EXISTS temp_tax_slabs;
		   		
		CREATE TEMP TABLE temp_tax_slabs  as 
		select 
			slab_id,
			"min" as min_limit,
			"max"  as max_limit,
			tax_rate,
			CAST (NULL AS numeric) AS amount
		from tax_slab order by slab_id;
		
		
		l_loction :=11;
		PERFORM public.sea_payroll_log_messages(p_cid,l_loction,'sea_get_tax_value','Temp Table created and data inserted into temp table from  tax_slab table ',l_loction::text);
		update temp_tax_slabs
		set amount=tax_rate*(min_limit-1)
		WHERE max_limit<=p_gross_value 
		AND max_limit IS NOT NULL;
		
		l_loction :=12;
		PERFORM public.sea_payroll_log_messages(p_cid,l_loction,'sea_get_tax_value','tax amount update for max  value IS not null records  ',l_loction::text);
		update temp_tax_slabs
		set amount=tax_rate*(p_gross_value-(min_limit-1))
		WHERE (p_gross_value <= max_limit or max_limit is null)
		AND   p_gross_value>=min_limit;
		
		l_loction :=13;
		PERFORM public.sea_payroll_log_messages(p_cid,l_loction,'sea_get_tax_value','tax amount update for max value IS null records ',l_loction::text);
		BEGIN 
		l_loction :=14;
			select coalesce(sum(amount) ,0) 
			into l_ret_tx_amount
			from temp_tax_slabs;
		
			IF NOT FOUND 
			THEN 
				l_ret_tx_amount :=0;
			END IF;
			
			IF l_ret_tx_amount < 0
			THEN 
				l_ret_tx_amount :=0;
			END IF;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;	
			PERFORM public.sea_payroll_log_error(p_cid,'sea_get_tax_value'::text,l_loction,SQLSTATE||' : '||SQLERRM);
		END ;
		PERFORM public.sea_payroll_log_messages(p_cid,l_loction,'sea_get_tax_value','Annual Tax value  ',l_ret_tx_amount::text);
		RETURN l_ret_tx_amount;
	
	exception
		WHEN OTHERS THEN
		RAISE INFO 'Error Name:%', SQLERRM;
		RAISE INFO 'Error State:%', SQLSTATE;	
		PERFORM public.sea_payroll_log_error(p_cid,'sea_get_tax_value'::text,l_loction,SQLSTATE||' : '||SQLERRM);
		RETURN 'Error ' || SQLSTATE || ':' || SQLERRM;
	
   END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_get_tax_value(integer, numeric)
  OWNER TO odoo;
