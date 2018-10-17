-- Function: public.sea_get_fiscal_year_start_date(date)

-- DROP FUNCTION public.sea_get_fiscal_year_start_date(date);

CREATE OR REPLACE FUNCTION public.sea_get_fiscal_year_start_date(p_date date)
  RETURNS date AS
$BODY$
		
DECLARE 
	ret_fyear_start_date date;
	v_year INT;
	v_month INT;
	
	BEGIN
		v_year := date_part('YEAR', p_date);
		v_month := date_part('MONTH', p_date);
		IF v_month < 4 
		THEN
			v_year := v_year-1;
		END IF;
		
		ret_fyear_start_date := v_year||'-04-01';
		RETURN ret_fyear_start_date;
			
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_get_fiscal_year_start_date(date)
  OWNER TO odoo;
