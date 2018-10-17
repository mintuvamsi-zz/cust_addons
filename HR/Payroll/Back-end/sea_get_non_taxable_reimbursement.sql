-- Function: public.sea_get_non_taxable_reimbursement(integer)

-- DROP FUNCTION public.sea_get_non_taxable_reimbursement(integer);

CREATE OR REPLACE FUNCTION public.sea_get_non_taxable_reimbursement(p_grade integer)
  RETURNS text AS
$BODY$

DECLARE 
		non_taxable_values TEXT;
	BEGIN

		SELECT
			meal_coupons || ',' || lta || ',' || fuel || ',' || telephone_bill || ',' || driver INTO non_taxable_values
		FROM
			"non_taxable_reimbursments"
		WHERE
			"job_grade_id" = p_grade;
		
		IF non_taxable_values IS NOT NULL 
		THEN
			RETURN non_taxable_values;
		ELSE
			RETURN 'Error Message: Grade '||p_grade|| ' does not exist.Please contact administrator';
		END IF;
	exception
         WHEN others THEN
            RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;
        RETURN 'Error Message: '||SQLSTATE|| '  ' ||SQLERRM;

		
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_get_non_taxable_reimbursement(integer)
  OWNER TO odoo;
