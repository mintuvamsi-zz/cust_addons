-- Function: public.sea_calculate_tds(integer)

-- DROP FUNCTION public.sea_calculate_tds(integer);

CREATE OR REPLACE FUNCTION public.sea_calculate_tds(p_id integer)
  RETURNS numeric AS
$BODY$

DECLARE
    
    v_sal decimal := 0;
	vsal decimal := 0;
    l_tax numeric := 0;
	l_ret_tax text;
    v_t3 decimal;
    v_t2 decimal;
    v_t1 decimal;
    v_sum_pt numeric DEFAULT 0;
	l_std_deduct numeric;
	l_nps_per numeric;
	l_e_cess numeric;
    v_employee_id integer;
    v_pt_count integer;
    v_pt_max integer;
    t_count integer DEFAULT 12;
    v_max_date date;
    v_sal_sum integer;
    v_sal_count integer;
    v_sal_max_date date;
    t_sal_count integer DEFAULT 12;
    v_sal_max integer;
	l_sec_exemption1_ret text  DEFAULT '' ;
	l_sec_exemption2_ret text ;
	l_sec_exemption3_ret text ;
	l_sec_exemption4_ret text ;
	l_sec_exemption5_ret text ;
	l_sec_exemption6_ret text ;
    l_sec_exemption1 numeric;
    l_sec_exemption2 numeric;
    l_sec_exemption3 numeric;
    l_sec_exemption4 numeric;
    l_sec_exemption5 numeric;
    l_sec_exemption6 numeric;
	v_excem1_1 numeric;
	v_excem2_1 numeric;
    v_nps_val numeric;
    v_nps_max numeric;
	l_any_other_deductions numeric;
    v_nps_cnt integer;
    v_nps_sum numeric;
    l_t_nps_cnt integer DEFAULT 12;
    v_nps_date date;
    v_year integer;
    fyear_start date;
	l_last_month date ;
	l_surcharge numeric;
	l_tds_amount numeric;
	l_prev_income numeric;
	l_prev_pt numeric;
	l_prev_tds numeric;
	l_e_cess_tax numeric;
	l_surcharge_tax numeric;
	l_avg_tds numeric;
	l_balance_tds numeric ;
	l_completed_months_cnt INTEGER;
	l_rem_months_cnt INTEGER;
	l_location integer :=0;
	l_tds_so_far numeric :=0;
	v_date_from date;
BEGIN
    /* SELECT TOTAL INTO v_pt FROM HR_PAYSLIP_LINE WHERE NAME LIKE 'Professional Tax%' AND CONTRACT_ID IN 
    (SELECT ID FROM HR_CONTRACT WHERE id =  p_id); */
    -- insert into test_message values(1,v_pt); 

		-- selecting the  payroll configurale values from  res_config_setting
	BEGIN
		l_location :=10;
		SELECT
			standard_deduction,
			national_pension_scheme,
			education_cess,
			sur_charge
			INTO l_std_deduct,
			l_nps_per,
			l_e_cess,
			l_surcharge
		FROM
			res_config_settings
		order by id 
		desc limit 1;
				RAISE NOTICE 'l_nps_per : %',l_nps_per;

		
		
		IF NOT FOUND 
		THEN 			
			l_std_deduct := 0;
			l_nps_per := 0;
			l_e_cess := 0;
			l_surcharge := 0;
			l_location :=20;
			
		END IF;
		l_location :=30;
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching configuration parameters standard_deduction  ',l_std_deduct::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching configuration parameters national_pension_scheme  ',l_nps_per::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching configuration parameters education_cess  ',l_e_cess::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching configuration parameters sur_charge  ',l_surcharge::text);
		
		l_location :=40;
		RAISE NOTICE 'Location : %',l_location;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
			
	END;
	
	RAISE NOTICE 'Location : %',l_location;
	RAISE NOTICE 'l_std_deduct : %,l_nps_per : %,l_e_cess : %,l_surcharge : %',l_std_deduct,l_nps_per,l_e_cess,l_surcharge;
	 -- get employee_id based on contract_id
	BEGIN
		l_location :=50;
		SELECT
			employee_id INTO v_employee_id
		FROM
			hr_contract hc,
			hr_payroll_structure hps,
			hr_structure_salary_rule_rel hsr,
			hr_salary_rule hsru
		WHERE
			hc.id = p_id
			AND hc.struct_id = hps.id
			AND hps.id = hsr.struct_id
			AND hsr.rule_id = hsru.id
			AND hsru.name = 'Tax Deducted at Source';
			
			
				RAISE NOTICE 'v_employee_id : %',v_employee_id;

		IF NOT FOUND 
		THEN 
			l_location :=60;
			PERFORM public.sea_raise_payroll_message('NO-TAX_DEDUCTED_AT_SOURCE',p_id,v_employee_id, current_date,'E');
			RETURN -11111;
		END IF;

		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching EmployeeId   ',v_employee_id::text);
		l_location :=70;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;	
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
	END;
	RAISE NOTICE 'Location : %',l_location;
	
		-- Employee CURRENT MONTH  payslip date  
	BEGIN
		l_location :=80;
		SELECT
			max(date_to) INTO v_sal_max_date
		FROM
			hr_payslip hp,
			hr_employee he,
			hr_payslip_line hpl
		WHERE
			hp.employee_id = he.id
			AND hpl.slip_id = hp.id
			AND hpl.name = 'Gross'
			AND he.id = v_employee_id
		GROUP BY
			he.id;
		IF NOT FOUND 
		THEN 		
			l_location :=90;
			PERFORM public.sea_raise_payroll_message('NO-GROSS',p_id,v_employee_id, current_date,'E');
			RETURN -11111;
		END IF;

		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds',' Fetching latest payslip generated date   ',v_sal_max_date::text);
		
		l_location :=100;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;	
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
	END;
	RAISE NOTICE 'Location : %',l_location;
	RAISE NOTICE 'v_sal_max_date : %',v_sal_max_date;
	-- get financial start date 
	fyear_start := public.sea_get_fiscal_year_start_date(v_sal_max_date::date);
    RAISE NOTICE 'fyear_start : %',  fyear_start;	

	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds',' Finding Financial Year Start Date ',fyear_start::text);

	l_location :=110;
		-- Employer paid gross amount ,no.of times after financial year start date  
		
	BEGIN
	l_location :=120;
		SELECT
			sum(amount),
			count(he.id),
			max(date_to)
			INTO v_sal_sum,
			v_sal_count,
			v_sal_max_date
		FROM
			hr_payslip hp,
			hr_employee he,
			hr_payslip_line hpl
		WHERE
			hp.employee_id = he.id
			AND hpl.slip_id = hp.id
			AND hpl.name = 'Gross'
			AND he.id = v_employee_id
			AND date_to >= fyear_start
		GROUP BY
			he.id;
		IF NOT FOUND 
		THEN 			
			l_location :=120;
			PERFORM public.sea_raise_payroll_message('NO-GROSS',p_id,v_employee_id, v_sal_max_date,'E');
			RETURN -11111;
		END IF;
		l_location :=130;
		
		
		l_location :=150;
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Employer Paid total Amount(inc.current month) ',v_sal_sum::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Employer Paid count  ',v_sal_count::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Employer Paid date ',v_sal_max_date::text);

		l_location :=160;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;	
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
	END;
	RAISE NOTICE 'Location : %',l_location;
	RAISE NOTICE 'v_sal_sum : %,v_sal_count : %,v_sal_max_date : %',v_sal_sum,v_sal_count,v_sal_max_date;
		-- current  month gross amount 
	
  	BEGIN
		l_location :=170;
		SELECT
			amount INTO v_sal_max
		FROM
			hr_payslip hp,
			hr_payslip_line hpl
		WHERE
			hpl.slip_id = hp.id
			AND hpl.name = 'Gross'
			AND hp.employee_id = v_employee_id
			AND date_to = v_sal_max_date;
		RAISE NOTICE 'current_month_sal : %', v_sal_max;
		IF NOT FOUND 
		THEN 			
			l_location :=180;
			PERFORM public.sea_raise_payroll_message('NO-GROSS',p_id,v_employee_id, v_sal_max_date,'E');
			RETURN -11111;
		END IF;
		l_location :=190;
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Employee current month Salary  ',v_sal_max::text);
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
	END;
	
	RAISE NOTICE 'Location : %',l_location;
		l_location :=200;
		-- Financial year start date 
	SELECT date_part ('year', f) * 12
      + date_part ('month', f) INTO v_sal_count
	FROM age (v_sal_max_date, fyear_start) f;
	
	RAISE NOTICE 'Months difference between current month  : %',v_sal_count;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Months difference between current month '||v_sal_max_date||' and Financial Year Start Date'||fyear_start,v_sal_count::text);
	l_location :=210;
    t_sal_count := t_sal_count - (v_sal_count+1);
    v_sal := v_sal_sum + (v_sal_max * t_sal_count);
    RAISE NOTICE 'Before excemptions, Gross Value: %  ', v_sal;

	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Employer to be pay months count  ',t_sal_count::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Employer Paying total Gross Amount ',v_sal::text);

	l_location :=220;
	RAISE NOTICE 'Location : %',l_location;
		-- Previous employer details
	BEGIN
		l_location :=230;
		SELECT
			income_received_previous_employee,
			previous_professional_tax,
			previous_employer_tds,
			any_other_deductions INTO l_prev_income,
			l_prev_pt,
			l_prev_tds,
			l_any_other_deductions
		FROM
			hr_contract 
		WHERE id = p_id;
		
		l_location :=240;
		IF NOT FOUND 
		THEN 			
			l_location :=250;
			l_prev_income := 0;
			l_prev_pt := 0;
			l_prev_tds := 0;
			l_any_other_deductions := 0;
		END IF;
		RAISE NOTICE 'l_prev_income : %,l_prev_pt : %,l_prev_tds : %',l_prev_income,l_prev_pt,l_prev_tds;
		
		l_location :=260;
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching Prev employer Details Prev.Income  ',l_prev_income::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching Prev employer Details Prev.ProfessionalTax  ',l_prev_pt::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching Prev employer Details Prev.TDS  ',l_prev_tds::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Fetching Additional Deduction Value   ',l_any_other_deductions::text);

		l_location :=270;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
	END;
	RAISE NOTICE 'Location : %',l_location;
	
	

		
	-- get paid professional tax 
	BEGIN
		
		l_location :=280;
		SELECT
			sum(amount),
			count(he.id),
			max(date_to) INTO v_sum_pt,
			v_pt_count,
			v_max_date
		FROM
			hr_payslip hp,
			hr_employee he,
			hr_payslip_line hpl
		WHERE
			hp.employee_id = he.id
			AND hpl.slip_id = hp.id
			AND hpl.name = 'Professional Tax'
			AND he.id = v_employee_id
			AND date_to >= fyear_start
		GROUP BY
			he.id;
		IF NOT FOUND 
		THEN 
			l_location :=290;
			v_sum_pt := 0;
			v_pt_count := 0;
			PERFORM public.sea_raise_payroll_message('NO-Professional Tax',p_id,v_employee_id, v_sal_max_date,'W');
		END IF;
		l_location :=300;
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','PT :  paid total PT amount  ',v_sum_pt::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','PT :   paid  PT months count  ',v_pt_count::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','PT :  paid  PT last date  ',v_max_date::text);
	
		l_location :=310;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;	
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
	END;
	RAISE NOTICE 'Location : %',l_location;
	RAISE NOTICE 'v_sum_pt : %,v_pt_count : %,v_max_date : %',v_sum_pt,v_pt_count,v_max_date;

	-- months defference between financial year start date and current month 
	SELECT date_part ('year', f) * 12
      + date_part ('month', f) INTO l_completed_months_cnt
	FROM age (v_max_date, fyear_start) f;
	l_location :=320;
		
    RAISE NOTICE 'v_sum_pt : %,v_pt_count : %,v_max_date : %,completed_months_cnt : % : ', v_sum_pt, v_pt_count, v_max_date,l_completed_months_cnt;
    l_rem_months_cnt := t_count - COALESCE(l_completed_months_cnt, 0);
	
		RAISE NOTICE 'l_rem_months_cnt : %',l_rem_months_cnt;

	t_count := t_count - COALESCE(l_completed_months_cnt+1, 0);
	l_location :=330;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','PT : Months difference between current month '||v_max_date||' and Financial Year Start Date'||fyear_start,l_completed_months_cnt::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','PT : Employer to Pay Months count',t_count::text);
	RAISE NOTICE 'Location : %',l_location;
	l_location :=340;
	BEGIN
		l_location :=350;
			-- get current month professional tax 
		SELECT
			amount INTO v_pt_max
		FROM
			hr_payslip hp,
			hr_payslip_line hpl
		WHERE
			hpl.slip_id = hp.id
			AND hpl.name = 'Professional Tax'
			AND hp.employee_id = v_employee_id
			AND date_to = v_max_date;
		IF NOT FOUND 
		THEN 
			l_location :=350;
			v_pt_max := 0;
			PERFORM public.sea_raise_payroll_message('NO-Professional Tax',p_id,v_employee_id, v_sal_max_date,'W');
		END IF;
		RAISE NOTICE 'v_pt_max : %,rem_months_cnt : %', v_pt_max,l_rem_months_cnt;
		
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','PT : Employee current month PT Value ',v_pt_max::text);

		l_location :=360;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;	
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
		
	END;
	RAISE NOTICE 'Location : %',l_location;
	RAISE NOTICE 'v_pt_max : %',v_pt_max;

	l_location :=370;
	 v_sum_pt := COALESCE(v_sum_pt, 0);
    --RAISE NOTICE 'After PT excemption, Gross Value: % ,v_sum_pt : %,v_pt_max :% ',v_sal,v_sum_pt,v_pt_max;
	RAISE NOTICE 'PT value : %,GrossValue : %',v_sum_pt,v_sal;
    v_sal := v_sal + v_sum_pt + (COALESCE(v_pt_max, 0) * t_count);
    RAISE NOTICE 'After PT excemption, Gross Value: % ,v_sum_pt : %,v_pt_max : %, t_count : %', v_sal,v_sum_pt,v_pt_max,t_count;
	l_location :=380;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','PT : After PT Total Gross Value ',v_sal::text);

	v_sal := v_sal-l_std_deduct;
	RAISE NOTICE 'After Standard deduction(Rs.%), Gross Value: %  ',l_std_deduct,v_sal;

	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','After Standard Deduction Total Gross Value ',v_sal::text);

	l_location :=390;
	RAISE NOTICE 'Location : %',l_location;
		-- Calculate Paid TDS amount 
	BEGIN
		l_location :=400;
		l_last_month := (date_trunc('month', v_sal_max_date::date) - interval '1 day')::date;
		SELECT
			COALESCE(ABS(sum(amount)),0) INTO l_tds_so_far
		FROM
			hr_payslip hp,
			hr_payslip_line hpl
		WHERE
			hp.id=hpl.slip_id
			AND hp.employee_id = hpl.employee_id
			AND hp.contract_id=hpl.contract_id
			AND hpl.code = 'TDS'
			AND hp.contract_id = p_id
			AND hp.employee_id = v_employee_id
			AND date_to>= fyear_start 
			AND date_to <= l_last_month
			AND hp.state='done';
			
		IF NOT FOUND 
		THEN 
			l_location :=410;
			l_tds_so_far := 0;
			PERFORM public.sea_raise_payroll_message('NO-TDS',p_id,v_employee_id, v_sal_max_date,'W');
		END IF;
		RAISE NOTICE 'Till last month( % ) tds value : % ',l_last_month,l_tds_so_far;
		

		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Employer Paid TDS amount  ',l_tds_so_far::text);

		l_location :=420;
		exception
			WHEN OTHERS THEN
			RAISE INFO 'Error Name:%', SQLERRM;
			RAISE INFO 'Error State:%', SQLSTATE;	
			PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
	
	END;
		
	RAISE NOTICE 'Location : %',l_location;
	RAISE NOTICE 'Previous Employer PT : %  ', COALESCE(l_prev_pt,0);
	RAISE NOTICE 'Previous Employer Income : %  ', COALESCE(l_prev_income,0);
	v_sal := v_sal + COALESCE(l_prev_income,0) - COALESCE(l_prev_pt,0);
	RAISE NOTICE 'After Previous Income & PT , Gross Value: %  ', v_sal;
	--RAISE NOTICE 'After Previous Income & PT , Gross Value: %  ', l_prev_income;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Gross Salary value after Previous Income and PT   ',v_sal::text);

		
	IF v_sal < 0 
	THEN 
		v_sal = 0;
	END IF;
	l_location :=430;
	
	RAISE NOTICE 'Location : %',l_location;
		 -- nps exemption 
		BEGIN
			l_location :=440;
			-- get paid nps amount
			SELECT
				sum(amount * (l_nps_per/100)),
				count(he.id),
				max(date_to) INTO v_nps_val,
				v_nps_cnt,
				v_nps_date
			FROM
				hr_payslip hp,
				hr_employee he,
				hr_payslip_line hpl
			WHERE
				hp.employee_id = he.id
				AND hpl.slip_id = hp.id
				AND hpl.name = 'Basic Salary'
				AND he.id = v_employee_id
				AND date_to >= fyear_start
			GROUP BY
				he.id;
			RAISE NOTICE 'Location : %',l_location;
			IF NOT FOUND 
			THEN 
				l_location :=450;
				v_nps_val := 0;
				v_nps_cnt := 0;
				PERFORM public.sea_raise_payroll_message('NO-Basic Salary',p_id,v_employee_id, v_sal_max_date,'E');
				RETURN -11111;
			END IF;
			RAISE NOTICE 'v_nps_val : %,v_nps_cnt : %,v_nps_date : %', v_nps_val, v_nps_cnt, v_nps_date;

			PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employer nps Paid  amount(10% basic salary)  ',v_nps_val::text);
			PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employer nps paid  count  ',v_nps_cnt::text);
			PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employer nps paid  date  ',v_nps_date::text);
			l_location :=460;
			RAISE NOTICE 'Location : %',l_location;
			exception
				WHEN OTHERS THEN
				RAISE INFO 'Error Name:%', SQLERRM;
				RAISE INFO 'Error State:%', SQLSTATE;	
				PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
		END;
			
		RAISE NOTICE 'Location : %',l_location;
			-- get current month nps amount 
		BEGIN
			l_location :=470;
			SELECT
				amount * (l_nps_per/100) INTO v_nps_max
			FROM
				hr_payslip hp,
				hr_payslip_line hpl
			WHERE
				hpl.slip_id = hp.id
				AND hpl.name = 'Basic Salary'
				AND hp.employee_id = v_employee_id
				AND date_to = v_nps_date;
				
			IF NOT FOUND 
			THEN 
				l_location :=480;
				v_nps_max := 0;
				PERFORM public.sea_raise_payroll_message('NO-Basic Salary',p_id,v_employee_id, v_sal_max_date,'E');
				RETURN -11111;
			END IF;
			l_location :=490;
			PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employee nps current month amount(10% basic salary)  ',v_nps_val::text);
			PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employer nps paid  count  ',v_nps_cnt::text);
			PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employer nps paid  date  ',v_nps_date::text);
			l_location :=500;
			exception
				WHEN OTHERS THEN
				RAISE INFO 'Error Name:%', SQLERRM;
				RAISE INFO 'Error State:%', SQLSTATE;	
				PERFORM public.sea_payroll_log_error(p_id,'sea_calculate_tds'::text,l_location,(SQLSTATE||' : '||SQLERRM)::text);
		END;
		RAISE NOTICE 'Location : %',l_location;
		
		
			--Months difference count between financial year start date and current  month
		SELECT date_part ('year', f) * 12
		+ date_part ('month', f) INTO v_nps_cnt
		FROM age (v_nps_date, fyear_start) f;
		l_location :=510;
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Months difference between current month '||v_nps_date||' and Financial Year Start Date'||fyear_start,v_nps_cnt::text);
		RAISE NOTICE 'Location : %',l_location;
		
		RAISE NOTICE 'v_nps_max : %,t_nps_cnt : %', v_nps_max, l_t_nps_cnt;
		l_t_nps_cnt = l_t_nps_cnt - (v_nps_cnt+1);
		RAISE NOTICE 't_nps_cnt : %', l_t_nps_cnt;
		v_nps_sum := v_nps_val + (v_nps_max * l_t_nps_cnt);
		RAISE NOTICE 'v_nps_sum : %,v_nps_val : %', v_nps_sum,v_nps_val;
		l_location :=520;
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employer to be pay months count  ',l_t_nps_cnt::text);
		PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','NPS : Employer Paying total NPS Amount ',v_nps_sum::text);
		l_location :=530;
		RAISE NOTICE 'Location : %',l_location;
	-- Updating all  excemption values in employee  investment declarations 
	PERFORM public.sea_tax_exemptions(p_id,v_employee_id);
	
	l_sec_exemption1_ret := public.sea_tax_exemption_section(p_id,v_employee_id,'Exemptions under section 10 & 17');
	--RAISE NOTICE 'l_sec_exemption1_ret : %',l_sec_exemption1_ret;
	IF l_sec_exemption1_ret ~ '^[0-9\.-]+$'  IS TRUE
	THEN 
		l_sec_exemption1 := l_sec_exemption1_ret::numeric;
		RAISE NOTICE 'l_sec_exemption1_ret : %, l_sec_exemption1 :% ',l_sec_exemption1_ret,l_sec_exemption1;
	END IF;
	--RAISE NOTICE 'l_sec_exemption1_ret : %, l_sec_exemption1 :% ',l_sec_exemption1_ret,l_sec_exemption1;
	
	l_sec_exemption2_ret := public.sea_tax_exemption_section(p_id,v_employee_id,'Home Loan Interest and property Income/Loss');
	IF l_sec_exemption2_ret ~ '^[0-9\.-]+$'  IS TRUE
	THEN 
		l_sec_exemption2 := l_sec_exemption2_ret::numeric;
		
	END IF;
	l_sec_exemption3_ret := public.sea_tax_exemption_section(p_id,v_employee_id,'Other income');
	IF l_sec_exemption3_ret ~ '^[0-9\.-]+$'  IS TRUE
	THEN 
		l_sec_exemption3 := l_sec_exemption3_ret::numeric;
		
	END IF;
	l_sec_exemption4_ret := public.sea_tax_exemption_section(p_id,v_employee_id,'Deductions under Chapter VI-A');
	IF l_sec_exemption4_ret ~ '^[0-9\.-]+$'  IS TRUE
	THEN 
		l_sec_exemption4 := l_sec_exemption4_ret::numeric;
		
	END IF;
	l_sec_exemption5_ret := public.sea_tax_exemption_section(p_id,v_employee_id,'Deductions under Chapter VI (sec 80C)');
	IF l_sec_exemption5_ret ~ '^[0-9\.-]+$'  IS TRUE
	THEN 
		l_sec_exemption5 := l_sec_exemption5_ret::numeric;
		
	END IF;
	l_sec_exemption6_ret := public.sea_tax_exemption_section(p_id,v_employee_id,'Deductions under Chapter VI (sec 80CCD)');
	IF l_sec_exemption6_ret ~ '^[0-9\.-]+$'  IS TRUE
	THEN 
		l_sec_exemption6 := l_sec_exemption6_ret::numeric;
		
	END IF;
	
	l_location :=540;
	l_sec_exemption6 := LEAST(v_nps_sum,l_sec_exemption6);
	RAISE NOTICE 'Location : %',l_location;
	
	-- Update NPS excemption value in employee  investment declarations 
	update  employee_taxlines etl
		SET allowed_limit = l_sec_exemption6 
		from employee_taxdeduction_header eth ,
		
		tds_taxdeductiontypes td
		where eth.employee_id = v_employee_id
		and eth.id=etl.employee_sectionlines
		and etl.deduction_desc=td.id
		and td.deduction_desc = 'National Pension scheme - Employee Contribution (sec 80CCD(1))' ;
	
		RAISE NOTICE 'v_sal : %',v_sal;

	RAISE NOTICE 'l_sec_exemption1 :%,l_sec_exemption2 : %,l_sec_exemption3 : %,l_sec_exemption4 : %,l_sec_exemption5 : %,l_sec_exemption6 : %',l_sec_exemption1,l_sec_exemption2,l_sec_exemption3,l_sec_exemption4,l_sec_exemption5,l_sec_exemption6;
	
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Tax exemption section 1 value  ',l_sec_exemption1::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Tax exemption section 2 value ',l_sec_exemption2::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Tax exemption section 3 value ',l_sec_exemption3::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Tax exemption section 4 value ',l_sec_exemption4::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Tax exemption section 5 value ',l_sec_exemption5::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Tax exemption section 6 value ',l_sec_exemption6::text);
	vsal := v_sal - l_sec_exemption1 + l_sec_exemption2 + l_sec_exemption3 - l_sec_exemption4 - l_sec_exemption5 - l_sec_exemption6;
	RAISE NOTICE ' Gross vsal after all exemptions : %',vsal;

		l_location :=550;
	if vsal < 0 
	then 
		vsal =0;
	end if;
	RAISE NOTICE 'Gross Salary After All exemptions  : %',vsal;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','GROSS Value After all exemptions ',vsal::text);
		
	vsal := vsal - l_any_other_deductions;
	RAISE NOTICE 'Other_deductions : %,Gross Value after Additional deductions : % ',l_any_other_deductions,vsal;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Other deductions values  ',l_any_other_deductions::text);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','GROSS Value After Other deductions values ',vsal::text);
	RAISE NOTICE 'Location : %',l_location;
	l_ret_tax := public.sea_get_tax_value(p_id,vsal);
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Annual Tax  ',l_ret_tax::text);
	l_location :=560;
	IF l_ret_tax ~ '^[0-9\.-]+$'  IS TRUE
	THEN 
		l_tax := l_ret_tax::numeric;
		l_location :=570;
	END IF;
	RAISE NOTICE 'Location : %',l_location;
	
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Tax value after applying tax slabs on Gross, Annual Tax   ',l_tax::text);
	RAISE NOTICE 'Location : %',l_location;
	
	RAISE NOTICE ' Tax value : %  ',l_tax;
    l_e_cess_tax := (l_tax * (l_e_cess/100));
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Education cess on Annual Tax   ',l_e_cess_tax::text);
	l_location :=580;
    RAISE NOTICE 'TDS value : % ,Education cess on TDS values : %  ',l_tax,l_e_cess_tax;
	
	l_surcharge_tax := (l_tax * (coalesce(l_surcharge,0)/100));
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Surcharge on Annual Tax   ',l_surcharge_tax::text);
	l_location :=590;
    l_tax := l_tax + l_e_cess_tax + l_surcharge_tax;
    RAISE NOTICE 'Surcharge on TDS is : %, After surcharge, Tax value per year : % , tilltds : %,PreviousTDS : %,rem_months_cnt : % ',l_surcharge_tax,l_tax,coalesce(l_tds_amount,0),l_prev_tds,l_rem_months_cnt;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds',' Annual tax value after adding education_cess & surcharge   ',l_tax::text);
	RAISE NOTICE 'Location : %',l_location;
	l_location :=600;
	
	/*IF l_tds_so_far = 0 
	THEN 
		l_tds_amount := (l_tax/12);
		
		RAISE NOTICE 'l_tds_amount : %',l_tds_amount;
		l_location :=610;
	END IF;*/
	
	-- adding current month tds value to tds deducted so far value 
	l_tds_amount = coalesce(l_tds_so_far,0) + (l_tax/12);
    PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','TDS Deducted So Far   ',l_tds_amount::text);
	
	

	l_balance_tds := l_tax - l_tds_so_far - coalesce(l_prev_tds,0);
	 
		RAISE NOTICE 'l_tax : %',l_tax;

		RAISE NOTICE 'l_tds_so_far : %',l_tds_so_far;
				RAISE NOTICE 'l_prev_tds : %',l_prev_tds;
	RAISE NOTICE 'l_balance_tds : %',l_balance_tds;

	l_location :=620;
	

	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Balance TDS   ',l_balance_tds::text);
	RAISE NOTICE 'l_balance_tds : %',l_balance_tds;

    IF l_balance_tds < 0
	THEN 
		l_balance_tds := 0;
	END IF;
	l_location :=630;
    PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','Remaining Months  ',l_rem_months_cnt::text);
	

	l_avg_tds := l_balance_tds/(l_rem_months_cnt) ;
	
			RAISE NOTICE 'l_rem_months_cnt : %',l_rem_months_cnt;

		RAISE NOTICE 'l_avg_tds : %',l_avg_tds;
	l_location :=640;
	PERFORM public.sea_payroll_log_messages(p_id,l_location,'sea_calculate_tds','TDS to be paid per month  ',l_avg_tds::text);
    IF l_avg_tds<0
	THEN 
		l_avg_tds := 0;
	END IF;
	
	
	RAISE NOTICE 'tds value after prev.tds and current employee tds : %',l_avg_tds;
	UPDATE
        hr_contract
    SET
        tds =  l_avg_tds,
        exemptions_undersection = l_sec_exemption1,
        income_chargeable_houseproperty = l_sec_exemption2,
        income_chargeable_otherhead_sources = l_sec_exemption3,
        deductions_underchapter_6a = l_sec_exemption4,
        deductions_under80c_80ccd = l_sec_exemption5 + l_sec_exemption6,
		net_taxable_income=vsal,
		--annual_tds_with_sur_cess_charges=round(l_tax,0),
		tds_upto_current_month_with_sur_cess_charges=coalesce(l_tds_amount,0),
		balance_tds_recovered_with_charges=l_balance_tds,
		avg_bal_tds_with_charges = l_avg_tds,
		deductions_under80c = l_sec_exemption5,
		standard_deduction = l_std_deduct
		--surcharge_on_income_tax = l_surcharge_tax,
		--education_cess = l_e_cess_tax
		
    WHERE
        id = p_id;
		l_location :=650;
		
	SELECT
		max(date_from) INTO v_date_from
	FROM
		hr_payslip
	WHERE
		employee_id = v_employee_id;
	RAISE NOTICE 'v_date_from: %',v_date_from;
	RAISE NOTICE 'p_id: %',p_id;
	RAISE NOTICE 'V_employee_id: %',v_employee_id;

	update hr_payslip 
	set	annual_tds_with_charges = round(l_tax,0),
			surcharge_on_income_tax = l_surcharge_tax,
			education_cess = l_e_cess_tax
	where employee_id = v_employee_id
	and  date_from = v_date_from  ; 

    RETURN round(l_avg_tds,0);
RAISE NOTICE 'l_avg_tds: %',l_avg_tds;END;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_calculate_tds(integer)
  OWNER TO odoo;
