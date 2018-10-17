-- Function: public.sea_payroll_calculate_components(integer)

-- DROP FUNCTION public.sea_payroll_calculate_components(integer);

CREATE OR REPLACE FUNCTION public.sea_payroll_calculate_components(p_cid integer)
  RETURNS text AS
$BODY$

DECLARE
    cnt INT DEFAULT 0;
	age_value interval;
    start_time TIME;
    end_time TIME;
    rec_hr_contract record;
    basic numeric DEFAULT 0;
    hra numeric DEFAULT 0;
    c_allowance numeric DEFAULT 0;
    epf numeric DEFAULT 0;
    erpf numeric DEFAULT 0;
    gdv numeric DEFAULT 0;
    p_bill numeric DEFAULT 0;
    lta_val numeric DEFAULT 0;
    t_bill numeric DEFAULT 0;
    f_pay numeric DEFAULT 0;
    gsal numeric DEFAULT 0;
    mv numeric DEFAULT 0;
    mi numeric DEFAULT 0;
	empr_esi numeric DEFAULT 0;
    emp_esi numeric DEFAULT 0;
    sp_allowance numeric DEFAULT 0;
    in_nontaxable_reimbursment numeric DEFAULT 0;
    driver_sal numeric DEFAULT 0;
    pt_val numeric DEFAULT 0;
	esi_limit_value numeric DEFAULT 0;
	ret_pt_val text;
    nps_val numeric DEFAULT 0;
	fp_percent numeric DEFAULT 0;
	epf_percent numeric DEFAULT 0;
	erpf_percent numeric DEFAULT 0;
	emp_esi_percent numeric DEFAULT 0;
	empr_esi_percent numeric DEFAULT 0;
	non_taxable_reimbursments_data TEXT;
	l_meal_allowance numeric;
    nt_reim record;
	error_message TEXT;
	ret_message TEXT;
	payroll_date date;
	cur_hr_contract CURSOR IS 
    SELECT
        cost_to_company,
        employeepf_exempt,
        employerspf_exempt,
        gratuity_exempt,
        petrolbill_exempt,
        lta_exempt,
        telephonebill_exempt,
        hra_exempt,
        flexiblepay_exempt,
        medicalinsurance_exempt,
        conveyanceallowance_exempt,
        employersesi_exempt,
        mealvouchers_exempt,
        struct_id,
		basic_salary_percentage,
		he.name ename,
		house_rent_allowance_metro_nonmetro,
		medical_insurance,
        grade,
        employeeesi_exempt,
        driver_salary_exempt,
        professional_tax_exempt
    FROM
        "hr_contract" hc,
        "hr_employee" he
    WHERE (employee_id = he.id)
    AND hc. "id" = p_cid ;
	
	cur_pt_slabs_data CURSOR IS 
	SELECT 
		"min", 
		"pt_amount"
	FROM "professional_tax_slab";
BEGIN
    start_time := CLOCK_TIMESTAMP();
	
	SELECT
		flexible_pay,
		employee_pf,
		employers_pf,
		employee_esi,
		employers_esi,
		esi_limit 
		INTO fp_percent,
		epf_percent,
		erpf_percent,
		emp_esi_percent,
		empr_esi_percent,
		esi_limit_value
	FROM
		res_config_settings
	ORDER BY
		id DESC
	LIMIT 1;	

	SELECT
		max(date_from) INTO payroll_date
	FROM
		hr_payslip
	WHERE
		contract_id = p_cid;
	
    FOR rec_hr_contract IN cur_hr_contract
	LOOP
	
        gsal := rec_hr_contract.cost_to_company / 12;
        
        IF EXISTS (
                SELECT
                    hsr.name,
                    hs.*
                FROM
                    hr_structure_salary_rule_rel hs
                    INNER JOIN hr_salary_rule hsr ON (hs.rule_id = hsr.id)
                WHERE
                    struct_id = rec_hr_contract.struct_id 
					AND hsr.code = 'BASIC') THEN
                basic := gsal * (rec_hr_contract.basic_salary_percentage::numeric/100);
        ELSE
			select public.sea_raise_payroll_message('NO-BASIC',p_cid, rec_hr_contract.ename, payroll_date) into ret_message;
            basic := 0;
        END IF;
		
        IF rec_hr_contract.gratuity_exempt IS FALSE THEN
            gdv := 0;
        ELSE
            gdv := ((basic / 26) * 15);
        END IF;
        
        IF EXISTS (
			SELECT
                   hsr.name,
                   hs.*
               FROM
                   hr_structure_salary_rule_rel hs
                   INNER JOIN hr_salary_rule hsr ON (hs.rule_id = hsr.id)
               WHERE
                   struct_id = rec_hr_contract.struct_id 
				AND hsr.code = 'HRAMN') THEN
				
               IF rec_hr_contract.hra_exempt IS FALSE THEN
					--select public.sea_raise_payroll_message('NO-HRAMN-PROVISION',p_cid, rec_hr_contract.ename, payroll_date)  into ret_message;;
					hra := 0;
               ELSE
                   hra := basic * (rec_hr_contract.house_rent_allowance_metro_nonmetro/100);
               END IF;
        ELSE
			----select public.sea_raise_payroll_message('NO-HRAMN',p_cid, rec_hr_contract.ename, payroll_date)  into ret_message;;
			hra := 0;
        END IF;
		
        -- Conveyance is not considering from 2018.
        c_allowance := 0;
        
		 -- Flexible allowance calculation
		        
				
				
		IF rec_hr_contract.flexiblepay_exempt IS FALSE THEN
			--select public.sea_raise_payroll_message('NO-HRAMN-PROVISION',p_cid, rec_hr_contract.ename, payroll_date)  into ret_message;;
			f_pay := 0;
		ELSE
                 f_pay := (rec_hr_contract.cost_to_company * (fp_percent/100)) / 12;
		END IF;
        
       
		
        IF EXISTS (
                SELECT
                    hsr.name,
                    hs.*
                FROM
                    hr_structure_salary_rule_rel hs
                    INNER JOIN hr_salary_rule hsr ON (hs.rule_id = hsr.id)
                WHERE
                    struct_id = rec_hr_contract.struct_id 
					AND hsr.code = 'EPMF') THEN
                
				IF rec_hr_contract.employeepf_exempt IS FALSE 
				THEN
					--select public.sea_raise_payroll_message('NO-EPMF-PROVISION',p_cid, rec_hr_contract.ename, payroll_date)  into ret_message;;	
                    epf := 0;
                ELSE
                    epf := (basic * (epf_percent/100));
                END IF;
        ELSE
			--select public.sea_raise_payroll_message('NO-EPMF',p_cid, rec_hr_contract.ename, payroll_date)  into ret_message;;	
            epf := 0;
        END IF;
        
        IF rec_hr_contract.employerspf_exempt IS FALSE THEN
			--select public.sea_raise_payroll_message('NO-EPF-PROVISION',p_cid, rec_hr_contract.ename, payroll_date)  into ret_message;;	
            erpf := 0;
        ELSE
            erpf := ROUND((basic * (erpf_percent/100)),0);
        END IF;
        
		
		
		
		
		RAISE NOTICE 'grade : % ', rec_hr_contract.grade;
		IF coalesce(char_length((trim(rec_hr_contract.grade))),0)=0
		THEN 
			RAISE NOTICE 'grade1 : % ', rec_hr_contract.grade;
			mv :=0;
			lta_val :=0;
			p_bill :=0;
			t_bill :=0;
			driver_sal :=0;
		ELSE
			select public.sea_get_non_taxable_reimbursement(rec_hr_contract.grade::int) into non_taxable_reimbursments_data;
			mv := SPLIT_PART(non_taxable_reimbursments_data,',',1)::numeric;
			lta_val := SPLIT_PART(non_taxable_reimbursments_data,',',2)::numeric;
			p_bill := SPLIT_PART(non_taxable_reimbursments_data,',',3)::numeric;
			t_bill := SPLIT_PART(non_taxable_reimbursments_data,',',4)::numeric;
			driver_sal := SPLIT_PART(non_taxable_reimbursments_data,',',4)::numeric;
		END IF;
        RAISE NOTICE 'mv : %,lta_val : %,p_bill : %,t_bill : %,driver_sal : %', mv,lta_val,p_bill,t_bill,driver_sal;

        IF gsal <= esi_limit_value THEN
            IF rec_hr_contract.employersesi_exempt IS FALSE THEN
				--select public.sea_raise_payroll_message('NO-EMPR-ESI-PROVISION',p_cid, rec_hr_contract.name, payroll_date)  into ret_message;;
                empr_esi := 0;
            ELSE
                empr_esi := (basic + hra + c_allowance) * empr_esi_percent/100;
            END IF;
        ELSE
            empr_esi := 0;
        END IF;
        
        IF gsal <= esi_limit_value THEN
            IF rec_hr_contract.employeeesi_exempt IS FALSE THEN
				--select public.sea_raise_payroll_message('NO-EMP-ESI-PROVISION',p_cid, rec_hr_contract.name, payroll_date)  into ret_message;;
                emp_esi := 0;
            ELSE
                emp_esi := (basic + hra + c_allowance) * emp_esi_percent/100;
            END IF;
        ELSE
            emp_esi := 0;
        END IF;
        
		
		 -- Adding  meal allowance value to Gross value 
		/*SELECT
            amount_fix into l_meal_allowance
        FROM
            hr_structure_salary_rule_rel hs
            INNER JOIN hr_salary_rule hsr ON (hs.rule_id = hsr.id)
        WHERE
            struct_id = rec_hr_contract.struct_id 
			AND hsr.code = 'MA';
		
		gsal := gsal + l_meal_allowance;*/
		
		
		select public.sea_get_pt_value(gsal) into ret_pt_val;
		IF ret_pt_val ~ '^[0-9\.]+$'  
		THEN 
			pt_val := ret_pt_val::numeric;
		END IF;
		
		
		
        in_nontaxable_reimbursment := (((lta_val + mv + p_bill + t_bill + driver_sal) / 12) + rec_hr_contract.medical_insurance);
        sp_allowance = gsal - basic - hra - c_allowance - f_pay - in_nontaxable_reimbursment - erpf - empr_esi - gdv / 12;
        RAISE NOTICE 'Id: %,gsal: %,basic : %,hra: %,c_allowance: %,epf: %,erpf: %,gratuity: %,p_bill: %,lta: %,mv : %,t_bill: %,driver_sal : %,f_pay: %,mi: %,wage: %,non_tx : %,s_all: %,empr_esi : %', p_cid, ROUND(gsal,2), ROUND(basic,0), ROUND(hra,0), c_allowance, ROUND(epf,0), ROUND(erpf,0), ROUND((gdv / 12), 0), ROUND(p_bill / 12,0), ROUND(lta_val / 12,0), ROUND(mv / 12,0), ROUND(t_bill / 12,0), ROUND(driver_sal / 12,0), ROUND(f_pay,0), rec_hr_contract.medical_insurance, ROUND(basic, 0), ROUND(in_nontaxable_reimbursment, 0), ROUND(sp_allowance, 0), ROUND(empr_esi, 0);
        gsal = basic + hra + c_allowance + f_pay + sp_allowance + in_nontaxable_reimbursment;
        
        RAISE NOTICE 'Gross Salary : % ', ROUND(gsal,2);
    END LOOP;
	
        UPDATE
            hr_contract
        SET
            conveyance_allowance = c_allowance,
            employee_pf = ROUND(epf, 0),
            employers_pf = ROUND(erpf, 0),
            gratuity = ROUND((gdv / 12),0),
            petrol_bill = p_bill / 12,
            lta = ROUND(lta_val / 12, 0),
            telephone_bill = ROUND(t_bill / 12, 0),
            flexible_pay = f_pay,
            --medical_insurance = mi,
			--hra_recieved = hra,
            meal_vouchers = ROUND(mv / 12, 0),
            special_allowance = ROUND(sp_allowance, 0),
            wage = ROUND(basic, 0),
            gross_salary = ROUND(gsal, 0), --+ROUND(nps_val,0)
            driver_salary = ROUND(driver_sal / 12, 0),
            nontaxable_reimbursment = in_nontaxable_reimbursment,
            professional_tax = ROUND(pt_val, 0),
            employee_esi = ROUND(emp_esi, 0),
            employers_esi = ROUND(empr_esi, 0)
        WHERE
            "id" = p_cid;
        GET DIAGNOSTICS cnt = ROW_COUNT;
        RAISE NOTICE '% Records effected in hr_contract', cnt;
        end_time := CLOCK_TIMESTAMP();
        age_value := end_time - start_time;
        RETURN age_value;
        exception
        WHEN others THEN
            RAISE INFO 'Error Name:%', SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
        RETURN 'Error ' || SQLSTATE || ':' || SQLERRM;
        END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_payroll_calculate_components(integer)
  OWNER TO odoo;
