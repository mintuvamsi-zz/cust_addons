-- Function: public.sea_tax_exemptions(integer, integer)

-- DROP FUNCTION public.sea_tax_exemptions(integer, integer);

CREATE OR REPLACE FUNCTION public.sea_tax_exemptions(
    p_cid integer,
    p_emp_id integer)
  RETURNS void AS
$BODY$

DECLARE 
	rec_tds_section record;
	rec_hr_contract record;
	l_produced_val numeric :=0;
	l_hra_pyear numeric :=0;
	l_hra_excemtion_val numeric :=0;
	l_location integer := 0;
	l_t_excemption numeric :=0;
	l_actual_hra_reduce_basic numeric :=0;
	l_lta_exemption numeric :=0;
	l_hra_reduces_basic_salary_percentage numeric :=0;
	l_permanent_disability_thershold integer :=0;
	l_disability_less_than_thershold integer :=0;
	l_disability_greater_than_thershold integer :=0;
	l_mi_exemption numeric :=0;
	l_donation_factor numeric :=0;
	l_date_from date;
	cur_hr_contract CURSOR IS 
	select 
		*
	from 
		hr_contract
	where id=p_cid;
	
	cur_tds_section CURSOR IS 
	SELECT
                    *
    FROM
        tds_taxdeductiontypes
	WHERE deductionlimit_type='C'
    ORDER BY
        id;
	BEGIN
	
		l_location :=10;
		
		BEGIN 
			select 
				hra_reduces_basic_salary_percentage,
				permanent_disability_thershold,
				disability_less_than_thershold,
				disability_greater_than_thershold,
				donations_for_funds_charities_factor
				into l_hra_reduces_basic_salary_percentage,
				l_permanent_disability_thershold,
				l_disability_less_than_thershold,
				l_disability_greater_than_thershold,
				l_donation_factor
			FROM res_config_settings
			order by id desc limit 1;
		
			IF NOT FOUND 
			THEN 
				l_hra_reduces_basic_salary_percentage :=0;
				l_permanent_disability_thershold  :=0;
				l_disability_less_than_thershold  :=0;
				l_disability_greater_than_thershold  :=0;
				l_donation_factor := 0;
			END IF;
		
		exception
			WHEN OTHERS THEN
				RAISE INFO 'Error Name:%', SQLERRM;
				RAISE INFO 'Error State:%', SQLSTATE;
				PERFORM public.sea_payroll_log_error(p_cid,'sea_tax_exemptions',l_location,SQLSTATE||' : '||SQLERRM);
		
		END;
	RAISE NOTICE 'Location : %',l_location;
	FOR rec_hr_contract IN cur_hr_contract
	LOOP
		FOR rec_tds_section IN cur_tds_section
		LOOP
						IF rec_tds_section.deduction_desc = 'HRA Exemption (sec 10 (13A))' THEN
                            l_hra_pyear = (rec_hr_contract.wage * COALESCE(rec_hr_contract.house_rent_allowance_metro_nonmetro/100,0)) * 12;
                            
							BEGIN
								l_location :=20;
								SELECT
									etl.amount INTO l_produced_val
								FROM
									"employee_taxdeduction_header" eth
									INNER JOIN employee_taxlines etl ON (eth.id = etl.employee_sectionlines)
								WHERE
									"employee_id" = p_emp_id
									AND etl.deduction_desc = rec_tds_section.id;
									
								IF NOT FOUND 
								THEN 
									l_produced_val := 0;
									l_location :=30;
								END IF;
								l_location :=40;
								PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions','HRA Exemption (sec 10 (13A)) : Fetching Employee declared Value for '||rec_tds_section.deduction_desc,l_produced_val::text);
								exception
									WHEN OTHERS THEN
									RAISE INFO 'Error Name:%', SQLERRM;
									RAISE INFO 'Error State:%', SQLSTATE;
									PERFORM public.sea_payroll_log_error(p_cid,l_location,'sea_tax_exemptions'::text,l_location,SQLSTATE||' : '||SQLERRM);
							END;
							
							RAISE NOTICE 'Location : %',l_location;
							l_actual_hra_reduce_basic = l_produced_val - ((rec_hr_contract.wage * (l_hra_reduces_basic_salary_percentage/100)) * 12);
                            
                            l_hra_excemtion_val := LEAST (l_hra_pyear,l_actual_hra_reduce_basic,l_hra_pyear) ;
							RAISE NOTICE 'hra_recieved : %,l_actual_hra_reduce_basic : %,l_hra_pyear : %',l_hra_pyear,l_actual_hra_reduce_basic,l_hra_pyear;
							PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions','HRA Exemption (sec 10 (13A)) : Calculated HRA Value ',l_hra_pyear::text);
							PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions','HRA Exemption (sec 10 (13A)) : Calculated actual_hra_reduce_basic Value ',l_actual_hra_reduce_basic::text);
							PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions','HRA Exemption (sec 10 (13A)) : Annual HRA received Value ',l_hra_pyear::text);
							PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions','HRA Exemption (sec 10 (13A)) : Least value in above four Values ',l_hra_excemtion_val::text);
								

							
							
							IF l_hra_excemtion_val<0
							THEN 
								l_hra_excemtion_val=0;
							END IF;
									
							RAISE NOTICE 'AnnualHRA_Rec : %,l_produced_val : %, l_hra_pyear : %,10per(Basic) : %,l_hra_excemtion_val : %',l_hra_pyear,l_produced_val,l_hra_pyear,((rec_hr_contract.wage * 0.1) * 12),l_hra_excemtion_val;
							
                            IF l_produced_val < l_hra_excemtion_val THEN
                                l_hra_excemtion_val := l_produced_val;
                            END IF;

							PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions',' Section '||rec_tds_section.deduction_desc||' Exemption Value ',l_hra_excemtion_val::text);
							
							UPDATE employee_taxlines etl
							SET  allowed_limit = l_hra_excemtion_val ,
									deduction_limit = l_hra_excemtion_val
							from employee_taxdeduction_header eth
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id=p_emp_id
							and etl.deduction_desc =  rec_tds_section.id;
							
                        END IF;
						
                        IF rec_tds_section.deduction_desc = 'Transport Exemption (sec 10(14))' THEN
                            RAISE NOTICE 'rec_hr_contract.petrol_bill : %,rec_tds_section.id : %', rec_hr_contract.petrol_bill, rec_tds_section.id;
							

							PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions',rec_tds_section.deduction_desc||':  Selected petrol_bill Value ',rec_hr_contract.petrol_bill::text);

							
                            IF rec_hr_contract.petrol_bill > 0 THEN
                                l_t_excemption := 0;
                            ELSE
                                l_t_excemption := coalesce(rec_hr_contract.conveyance_allowance,0) * 12;
                                BEGIN
								l_location := 30;
									SELECT
										etl.amount INTO l_produced_val
									FROM
										"employee_taxdeduction_header" eth
										INNER JOIN employee_taxlines etl ON (eth.id = etl.employee_sectionlines)
									WHERE
										"employee_id" = p_emp_id
										AND etl.deduction_desc = rec_tds_section.id;
									
									IF NOT FOUND 
									THEN 
										l_produced_val := 0;
									END IF;
									
									PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions',' Selected petrol_bill Value ',rec_hr_contract.petrol_bill::text);
								exception
									WHEN OTHERS THEN
									RAISE INFO 'Error Name:%', SQLERRM;
									RAISE INFO 'Error State:%', SQLSTATE;
									PERFORM public.sea_payroll_log_error(p_cid,'sea_tax_exemptions'::text,l_location,SQLSTATE||' : '||SQLERRM);
								END;
								
                                RAISE NOTICE 't_excemption: %,l_produced_val : %', l_t_excemption, l_produced_val;
                                IF l_produced_val < l_t_excemption THEN
                                    l_t_excemption := coalesce(l_produced_val,0);
                                END IF;

								PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions',' Calculated t_excemption Value ',l_t_excemption::text);
								PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_tax_exemptions',' Employee declared amount Value ',l_produced_val::text);

                            END IF;
							
							UPDATE employee_taxlines etl
							SET  allowed_limit = l_t_excemption ,
									deduction_limit = l_t_excemption
							from employee_taxdeduction_header eth
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id=p_emp_id
							and etl.deduction_desc =  rec_tds_section.id;
							
							
                        END IF;
						/*
                        IF rec_tds_section.deduction_desc = 'Other exemptions under sec 10 (10) (gratuity, etc.)' THEN
							
							IF log_flag IS TRUE 
							THEN
								PERFORM public.sea_payroll_log_messages(p_cid,l_location,'sea_section_tax_exemption_value',' Selected gratuity Value ',rec_hr_contract.gratuity::text);
							END IF; 
							
                            IF rec_hr_contract.gratuity > 0 THEN
                                gt_exemption := 0;
                            ELSE
								BEGIN
									SELECT
										etl.amount INTO l_produced_val
									FROM
										"employee_taxdeduction_header" eth
										INNER JOIN employee_taxlines etl ON (eth.id = etl.employee_sectionlines)
									WHERE
										"employee_id" = p_emp_id
										AND etl.deduction_desc = rec_tds_section.id;
									
									IF NOT FOUND 
									THEN 
										l_produced_val := 0;
									END IF;
									gt_exemption := l_produced_val;
								exception
									WHEN OTHERS THEN
									RAISE INFO 'Error Name:%', SQLERRM;
									RAISE INFO 'Error State:%', SQLSTATE;	
								
								END;
                            END IF;
                        END IF;
						*/
                        IF rec_tds_section.deduction_desc = 'Medical Bills Exemption (sec 17(2))' THEN
                            IF rec_hr_contract.medical_insurance > 0 THEN
                                l_mi_exemption := 0;
                            ELSE
                                l_mi_exemption = rec_tds_section.deduction_limit;
								BEGIN
									
									SELECT
										etl.amount INTO l_produced_val
									FROM
										"employee_taxdeduction_header" eth
										INNER JOIN employee_taxlines etl ON (eth.id = etl.employee_sectionlines)
									WHERE
										"employee_id" = p_emp_id
										AND etl.deduction_desc = rec_tds_section.id;
									
									IF NOT FOUND 
									THEN 
										l_produced_val := 0;
									END IF;	
									
									exception
										WHEN OTHERS THEN
										RAISE INFO 'Error Name:%', SQLERRM;
										RAISE INFO 'Error State:%', SQLSTATE;	
								END;
								
                                IF l_produced_val < l_mi_exemption THEN
                                    l_mi_exemption := l_produced_val;
                                END IF;
                            END IF;
							
							UPDATE employee_taxlines etl
							SET  allowed_limit = COALESCE(l_mi_exemption ,0),
									deduction_limit = COALESCE(l_mi_exemption ,0)
							from employee_taxdeduction_header eth
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id=p_emp_id
							and etl.deduction_desc =  rec_tds_section.id;
						
                        END IF;
						
                        IF rec_tds_section.deduction_desc = 'LTA exemption (sec 10(5))' THEN
                            IF rec_hr_contract.lta > 0 THEN
                                l_lta_exemption := 0;
                            ELSE
                                -- lta=0 in hr_contract then exemption value also 0
                                l_lta_exemption := rec_hr_contract.lta * 12;
								BEGIN
									l_location :=40;
									SELECT
										etl.amount INTO l_produced_val
									FROM
										"employee_taxdeduction_header" eth
										INNER JOIN employee_taxlines etl ON (eth.id = etl.employee_sectionlines)
									WHERE
										"employee_id" = p_emp_id
										AND etl.deduction_desc = rec_tds_section.id;
										
									IF NOT FOUND 
									THEN 
										l_produced_val := 0;
									END IF;	
									
									exception
										WHEN OTHERS THEN
										RAISE INFO 'Error Name:%', SQLERRM;
										RAISE INFO 'Error State:%', SQLSTATE;	
										PERFORM public.sea_payroll_log_error(p_cid,'sea_tax_exemptions'::text,l_location,SQLSTATE||' : '||SQLERRM);
								END;
                                IF l_produced_val < l_lta_exemption THEN
                                    l_lta_exemption := l_produced_val;
                                END IF;
                            END IF;
							
							UPDATE employee_taxlines etl
							SET  allowed_limit = COALESCE(l_lta_exemption ,0)
							from employee_taxdeduction_header eth
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id=p_emp_id
							and etl.deduction_desc =  rec_tds_section.id;
							
                        END IF;
						

						
						IF rec_tds_section.deduction_desc = 'Deduction for permanent disability (sec 80U)' THEN
							
								UPDATE employee_taxlines  etl
								SET  allowed_limit = LEAST(amount,(CASE 
																	WHEN factor <= COALESCE(l_permanent_disability_thershold,0) THEN COALESCE(l_disability_less_than_thershold,0)
																	WHEN factor > COALESCE(l_permanent_disability_thershold,0) THEN COALESCE(l_disability_greater_than_thershold,0)
																	ELSE 0
																END )),
										deduction_limit = CASE 
																	WHEN factor <= COALESCE(l_permanent_disability_thershold,0) THEN COALESCE(l_disability_less_than_thershold,0)
																	WHEN factor > COALESCE(l_permanent_disability_thershold,0) THEN COALESCE(l_disability_greater_than_thershold,0)
																	ELSE 0
																END 
								
								from employee_taxdeduction_header eth
								WHERE eth.id = etl.employee_sectionlines 
								and eth.employee_id=p_emp_id
								and etl.deduction_desc =  rec_tds_section.id;
						
						END IF;
						

						IF rec_tds_section.deduction_desc = 'Donation to approved fund and charities (sec 80G)' THEN
							UPDATE employee_taxlines etl
							SET  allowed_limit =  CASE 
																WHEN factor <= l_donation_factor THEN COALESCE((amount * l_donation_factor)/100,0)
																WHEN factor > l_donation_factor THEN COALESCE((amount * factor)/100,0)	
															END ,
									deduction_limit = CASE 
																WHEN factor <= l_donation_factor THEN COALESCE((amount * l_donation_factor)/100,0)
																WHEN factor > l_donation_factor THEN COALESCE((amount * factor)/100,0)	
															  END 
							from employee_taxdeduction_header eth
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id=p_emp_id
							and etl.deduction_desc =  rec_tds_section.id;
						
						END IF;
						
						IF rec_tds_section.deduction_desc = 'National Pension scheme - Employee Contribution (sec 80CCD(1))' THEN
							UPDATE employee_taxlines etl
							SET  allowed_limit = COALESCE(amount ,0)
							from employee_taxdeduction_header eth
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id=p_emp_id
							and etl.deduction_desc =  rec_tds_section.id;
						
						END IF;
						
						
						 
		
		END LOOP;
	END LOOP;
	   -- Fixed and Individual 

			update employee_taxlines	etl		
			set allowed_limit = COALESCE(least(etl.deduction_limit,etl.amount),0)		
			from employee_taxdeduction_header eth
			where eth.id=etl.employee_sectionlines 
			and eth.employee_id=p_emp_id
			and limit_level='I'
			and deduction_desc in ( select id from tds_taxdeductiontypes			
										where deductionlimit_type ='F');
		--Section Level

		update employee_taxlines etl
		set allowed_limit =  COALESCE(least(deduction_limit,( select sum(amount) from employee_taxlines b
							where b.employee_sectionlines=etl.employee_sectionlines
							and b.section_id=etl.section_id)),0)
		from employee_taxdeduction_header eth
		where eth.id=etl.employee_sectionlines 
		and eth.employee_id=p_emp_id
		and  etl.section_id = 'Deductions under Chapter VI (sec 80C)'
		and limit_level='S';
		
		-- Section level for Other Income
		
		WITH oi_intrest_house_income  as (
							select amount amt1  
							from  employee_taxlines etl,					
							 employee_taxdeduction_header eth,
							 tds_taxdeductiontypes td
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id=p_emp_id
							and etl.deduction_desc=td.id
							and td.deduction_desc =  'House/property income or loss (enter loss as negative)'
		), oi_intrest_house_loan as (
							select etl.id id1, amount amt2 ,td.deduction_limit  as deduction_limit1
							from  employee_taxlines etl,					
							 employee_taxdeduction_header eth,
							tds_taxdeductiontypes td
							WHERE eth.id = etl.employee_sectionlines 
							and eth.employee_id = p_emp_id
							and etl.deduction_desc=td.id
							and etl.limit_level='S'
							and td.deduction_desc =  'Interest on housing loan (for tax exemption)'
	) UPDATE employee_taxlines 
	set allowed_limit = GREATEST(amt1-amt2,-deduction_limit1,-amt2) 
	from oi_intrest_house_income ,
	oi_intrest_house_loan
	where id=oi_intrest_house_loan.id1 ;

		
			   -- infinity limit 

		update employee_taxlines	etl		
		set allowed_limit = COALESCE(etl.amount,0),		
			  deduction_limit = COALESCE(etl.amount,0)	
		from employee_taxdeduction_header eth
		where eth.id=etl.employee_sectionlines 
		and eth.employee_id=p_emp_id
		and limit_level='I'
		and deduction_desc in ( select id from tds_taxdeductiontypes			
										where deductionlimit_type ='N');
		
		-- Updating following values only for showing in Payslip
	/*	
		UPDATE hr_contract 
		set hra_exemption = COALESCE(l_hra_excemtion_val,0),
		--actualhra_reduces_basic = l_actual_hra_reduce_basic,
		--hra_40percent = l_hra_pyear,
		--hra_recieved = l_hra_pyear,
		house_property_income_loss = (select allowed_limit 
														from employee_taxdeduction_header eth ,
														employee_taxlines etl,
														tds_taxdeductiontypes td
														where eth.employee_id = p_emp_id
														and eth.id=etl.employee_sectionlines
														and etl.deduction_desc=td.id
														and td.deduction_desc = 'House/property income or loss (enter loss as negative)'),
		providentfund_80c = (select amount 
										from employee_taxdeduction_header eth ,
										employee_taxlines etl,
										tds_taxdeductiontypes td
										where eth.employee_id = p_emp_id
										and eth.id=etl.employee_sectionlines
										and etl.deduction_desc=td.id
										and td.deduction_desc = 'Employees Provident Fund & Voluntary PF (sec 80C)'),
		"housing_loan_principal_amount_80C" =  (select amount 
																	from employee_taxdeduction_header eth ,
																	employee_taxlines etl,
																	tds_taxdeductiontypes td
																	where eth.employee_id = p_emp_id
																	and eth.id=etl.employee_sectionlines
																	and etl.deduction_desc=td.id
																	and td.deduction_desc =  'Housing loan principal repayment, regn/stamp duty (sec 80C)'),
		
		any_other_deductions = (select allowed_limit 
											from employee_taxdeduction_header eth ,
											employee_taxlines etl,
											tds_taxdeductiontypes td
											where eth.employee_id = p_emp_id
											and eth.id=etl.employee_sectionlines
											and etl.deduction_desc=td.id
											and td.deduction_desc = 'Any other deductions (incl. donations u/s 35AC/80GGA)')
		where id = p_cid;*/
		-----------------------------------------------------------------------------
		select max(date_from) into 	l_date_from from hr_payslip where employee_id = p_emp_id;
	 	RAISE NOTICE 'l_date_from: %',l_date_from;
		RAISE NOTICE 'p_cid: %',p_cid;
		RAISE NOTICE 'p_emp_id: %',p_emp_id;

	update hr_payslip 
	set 	"housing_loan_principal_amount_80C" = (select amount 
																from employee_taxdeduction_header eth ,
																employee_taxlines etl,
																tds_taxdeductiontypes td
																where eth.employee_id = p_emp_id
																and eth.id=etl.employee_sectionlines
																and etl.deduction_desc=td.id
																and td.deduction_desc =  'Housing loan principal repayment, regn/stamp duty (sec 80C)'
																)	,
			providentfund_80c = (select amount 
									from employee_taxdeduction_header eth ,
									employee_taxlines etl,
									tds_taxdeductiontypes td
									where eth.employee_id = p_emp_id
									and eth.id=etl.employee_sectionlines
									and etl.deduction_desc=td.id
									and td.deduction_desc = 'Employees Provident Fund & Voluntary PF (sec 80C)'),
			--surcharge_on_income_tax = l_surcharge_tax,
			--education_cess = l_e_cess_tax,
			actualhra_reduces_basic = l_actual_hra_reduce_basic,
			hra_40percent = l_hra_pyear,		
			annual_hra_received = l_hra_pyear,
			hra_exemption = COALESCE(l_hra_excemtion_val,0)	
	where employee_id = p_emp_id
	and  date_from = l_date_from  ; 
		
		
		
		
    END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.sea_tax_exemptions(integer, integer)
  OWNER TO odoo;
