-- Function: public.sea_get_pt_value(numeric)

-- DROP FUNCTION public.sea_get_pt_value(numeric);

CREATE OR REPLACE FUNCTION public.sea_get_pt_value(p_gross_value numeric)
  RETURNS text AS
$BODY$

DECLARE 
		ret_pt_amount numeric;
	BEGIN


	select pt_amount into ret_pt_amount
	from professional_tax_slab
		where (p_gross_value between min and max) OR (p_gross_value between min and max IS NULL);
	
		IF NOT FOUND 
		THEN 
			RETURN '0';
		ELSE
			RETURN ret_pt_amount;
		END IF;
	exception
         WHEN others THEN
            RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;
        RETURN 'Message '||p_gross_value|| ' No PT slab defined for given  gross value ';

		
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_get_pt_value(numeric)
  OWNER TO odoo;
