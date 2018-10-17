-- Function: public.tds_deduction_val(integer, integer, text)

-- DROP FUNCTION public.tds_deduction_val(integer, integer, text);

CREATE OR REPLACE FUNCTION public.tds_deduction_val(
    p_contract_id integer,
    p_emp_id integer,
    p_section_type text)
  RETURNS numeric AS
$BODY$

 DECLARE cnt INT DEFAULT 0;
 DECLARE age_value interval ;
 DECLARE start_time TIME ;
 DECLARE end_time TIME ;
 DECLARE V_val numeric default 0;
 DECLARE produced_val numeric default 0;
 DECLARE t_excemption numeric default 0;
 DECLARE gt_exemption numeric default 0;
 DECLARE mi_exemption numeric default 0;
 DECLARE lta_exemption numeric default 0;
 DECLARE hra_excemtion_val numeric default 0;
 DECLARE house_loan_exemption numeric default 0;
 DECLARE mi_premium_exemption numeric default 0;
 DECLARE mi_parents numeric default 0;
 DECLARE mi_handicapped numeric default 0;
 DECLARE mi_diseases numeric default 0;
 DECLARE education_loan numeric default 0;
 DECLARE sb_interest numeric default 0;
 DECLARE permanent_exemption numeric default 0;
 DECLARE other_deductions numeric default 0;
 DECLARE hra_pyear numeric default 0;
 DECLARE p_house_loan_exemption numeric default 0;
 DECLARE house_property_exemption numeric default 0;
 DECLARE donation numeric default 0;
 DECLARE limit_value numeric default 0;
 DECLARE deduction_80c numeric default 0;
 DECLARE deduction_80d numeric default 0;
 DECLARE other_income_limit numeric default 0;
 DECLARE tax_id INT DEFAULT 0;
 
 
 rec_tax_data  record;
 rec_hr_contract  record;
 rec_tds_sections  record;
 
BEGIN
--start_time:=CLOCK_TIMESTAMP();
RAISE NOTICE 'empid: %, sec_type : %',p_emp_id,p_section_type;
FOR rec_hr_contract IN SELECT * FROM "hr_contract" where id=p_contract_id
LOOP
	IF p_section_type='Exemptions under section 10 & 17' THEN
		FOR rec_tds_sections IN select *from tds_taxdeductiontypes where sectiontypes=p_section_type ORDER BY id
		LOOP
			IF rec_tds_sections.deduction_desc='HRA Exemption (sec 10 (13A))' 
			THEN 
				hra_pyear=(rec_hr_contract.wage*0.4)*12;
				
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				
				
				select LEAST(rec_hr_contract.hra_recieved,   produced_val-((rec_hr_contract.wage*0.1)*12),hra_pyear) into hra_excemtion_val ;
				IF produced_val<hra_excemtion_val THEN 
					hra_excemtion_val:=produced_val;
				END IF;
				
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Transport Exemption (sec 10(14))' 
			THEN 
				RAISE NOTICE 'rec_hr_contract.petrol_bill : %,rec_tds_sections.id : %',rec_hr_contract.petrol_bill,rec_tds_sections.id;
				IF rec_hr_contract.petrol_bill>0 
				THEN 
					t_excemption:=0;
				ELSE 
					t_excemption:=NULLIF(rec_hr_contract.conveyance_allowance,0)*12;
					
					select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
					INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
					WHERE "employee_id" = p_emp_id 
					and etl.deduction_desc=rec_tds_sections.id;
					
					RAISE NOTICE 't_excemption: %,produced_val : %',t_excemption,produced_val;
					IF produced_val<t_excemption
					THEN 
						t_excemption:=produced_val;
					END IF;
				END IF;
				
				
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Other exemptions under sec 10 (10) (gratuity, etc.)' 
			THEN 
				IF rec_hr_contract.gratuity>0 
				THEN 
					gt_exemption:=0;
				ELSE 
					select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
					INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
					WHERE "employee_id" = p_emp_id 
					and etl.deduction_desc=rec_tds_sections.id;
					gt_exemption:=produced_val;
				END IF;
				
			
			END IF;
	
			IF rec_tds_sections.deduction_desc='Medical Bills Exemption (sec 17(2))' 
			THEN 
				IF rec_hr_contract.medical_insurance>0 
				THEN 
					mi_exemption:=0;
				ELSE 
					mi_exemption=rec_tds_sections.deduction_limit;
					select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
					INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
					WHERE "employee_id" = p_emp_id 
					and etl.deduction_desc=rec_tds_sections.id;
					
					IF produced_val<mi_exemption
					THEN 
						mi_exemption:=produced_val;
					END IF;
				END IF;
			END IF;
			
			IF rec_tds_sections.deduction_desc='LTA exemption (sec 10(5))' 
			THEN 
				IF rec_hr_contract.lta>0 
				THEN 
					lta_exemption:=0;
				ELSE 
					-- lta=0 in hr_contract then exemption value also 0
					lta_exemption:=rec_hr_contract.lta*12;
					select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
					INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
					WHERE "employee_id" = p_emp_id 
					and etl.deduction_desc=rec_tds_sections.id;
					
					IF produced_val<lta_exemption
					THEN 
						lta_exemption:=produced_val;
				
					END IF;
					
					
				END IF;
				
			END IF;
				
			
		END lOOP;
		
		V_val:=lta_exemption+mi_exemption+gt_exemption+t_excemption+hra_excemtion_val;
		RAISE NOTICE 'lta_exemption: %,mi_exemption : %,gt_exemption : %,t_excemption : %,hra_excemtion_val : %,V_val : %',lta_exemption,mi_exemption,gt_exemption,t_excemption,hra_excemtion_val,V_val;
	ELSIF p_section_type='Home Loan Interest and property Income/Loss' THEN
		FOR rec_tds_sections IN select *from tds_taxdeductiontypes where sectiontypes=p_section_type ORDER BY id
		LOOP
			IF rec_tds_sections.deduction_desc='House/property income or loss (enter loss as negative)' 
			THEN 
				select etl.amount into house_property_exemption FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				--select amount into  from employee_taxlines where section_id=p_section_type and deduction_desc=rec_tds_sections.id;
			END IF;
			
			
			IF rec_tds_sections.deduction_desc='Interest on housing loan (for tax exemption)' 
			THEN 
				--rec_tds_sections.deduction_limit;
				--select amount into p_house_loan_exemption from employee_taxlines where section_id=p_section_type and deduction_desc=rec_tds_sections.id;
				select etl.amount into p_house_loan_exemption FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				IF p_house_loan_exemption<rec_tds_sections.deduction_limit THEN 
					house_loan_exemption:=p_house_loan_exemption;
				ELSE 
					house_loan_exemption:=rec_tds_sections.deduction_limit;
				END IF;
			END IF;
				
			
		END LOOP;
				
		V_val:=coalesce(house_loan_exemption,0)+coalesce(house_property_exemption,0);
		RAISE NOTICE 'house_loan_exemption: %,house_property_exemption : %,V_val : %',coalesce(house_loan_exemption,0),coalesce(house_property_exemption,0),V_val;
	ELSIF p_section_type='Other income' THEN
		SELECT sum(etl.amount) into other_income_limit
		FROM "employee_taxdeduction_header" eth
		INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
		WHERE "employee_id" = p_emp_id and etl.section_id=p_section_type;

		V_val:=coalesce(other_income_limit,0);
		RAISE NOTICE 'other_income_limit: %,V_val : %',coalesce(other_income_limit,0),V_val;
		
	ELSIF p_section_type='Deductions under Chapter VI-A' THEN
		FOR rec_tds_sections IN select *from tds_taxdeductiontypes where sectiontypes=p_section_type ORDER BY id
		LOOP
			IF rec_tds_sections.deduction_desc='Medical Insurance Premium / health check (sec 80D)' 
			THEN 
				
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				
				IF coalesce(produced_val,0)<rec_tds_sections.deduction_limit THEN 
					mi_premium_exemption:=coalesce(produced_val,0);
				ELSE 
					mi_premium_exemption:=coalesce(rec_tds_sections.deduction_limit,0);
				
				END IF;
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Medical Insurance Premium for parents (sec 80D)' 
			THEN 
				
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				
				IF coalesce(produced_val,0)<coalesce(rec_tds_sections.deduction_limit,0) THEN 
					mi_parents:=coalesce(produced_val,0);
				ELSE 
					mi_parents:=coalesce(rec_tds_sections.deduction_limit,0);
				
				END IF;
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Medical for handicapped dependents (sec 80DD)' 
			THEN 
				
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				
				IF coalesce(produced_val,0)<coalesce(rec_tds_sections.deduction_limit,0) THEN 
					mi_handicapped:=coalesce(produced_val,0);
				ELSE 
					mi_handicapped:=coalesce(rec_tds_sections.deduction_limit,0);
				
				END IF;
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Medical for specified diseases (sec 80DDB)' 
			THEN 
				
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				
				IF coalesce(produced_val,0)<rec_tds_sections.deduction_limit THEN 
					mi_diseases:=coalesce(produced_val,0);
				ELSE 
					mi_diseases:=rec_tds_sections.deduction_limit;
				END IF;
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Higher Education Loan Interest Repayment (sec 80E)' 
			THEN 
				--select amount into produced_val from employee_taxlines where section_id=p_section_type and deduction_desc=rec_tds_sections.id;
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				education_loan:=coalesce(produced_val,0);
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Donation to approved fund and charities (sec 80G)' 
			THEN 
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				
				donation:=coalesce(produced_val,0)*0.5;
				
			END IF;
			IF rec_tds_sections.deduction_desc='Savings Bank interest exemption (sec 80TTA)' 
			THEN 
				select etl.amount into produced_val FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				
				IF coalesce(produced_val,0)<rec_tds_sections.deduction_limit  THEN 
					sb_interest:=coalesce(produced_val,0);
				ELSE 
					sb_interest:=rec_tds_sections.deduction_limit;
				END IF;
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Deduction for permanent disability (sec 80U)'  
			THEN 
				
				select etl.amount,etl.deduction_limit into produced_val,limit_value FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				RAISE NOTICE 'rec_tds_sections.id : %,deduction_limit : %,produced_val : %',rec_tds_sections.id,limit_value,produced_val;
				IF coalesce(produced_val,0)<coalesce(limit_value,0)  THEN 
					permanent_exemption:=coalesce(produced_val,0);
				ELSE 
					permanent_exemption:=coalesce(limit_value,0);
				END IF;
				
			END IF;
			
			IF rec_tds_sections.deduction_desc='Any other deductions (incl. donations u/s 35AC/80GGA)' 
			THEN 
				select etl.amount,etl.deduction_limit into produced_val,limit_value FROM "employee_taxdeduction_header" eth
				INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
				WHERE "employee_id" = p_emp_id 
				and etl.deduction_desc=rec_tds_sections.id;
				RAISE NOTICE 'rec_tds_sections.id : %,deduction_limit : %,produced_val : %',rec_tds_sections.id,limit_value,produced_val;
				
				IF coalesce(produced_val,0)<coalesce(limit_value,0)  THEN 
					other_deductions:=coalesce(produced_val,0);
				ELSE 
					other_deductions:=coalesce(limit_value,0);
				END IF;
				
			END IF;
			
			
		END LOOP;
		V_val:=mi_premium_exemption+mi_parents+mi_handicapped+mi_diseases+education_loan+donation+sb_interest+permanent_exemption+other_deductions;
		RAISE NOTICE 'mi_premium_exemption: %,mi_parents : %,mi_handicapped  :%,mi_diseases  :%,education_loan : %,donation : %,sb_interest : %,permanent_exemption : %,other_deductions : %,V_val : %',mi_premium_exemption,mi_parents,mi_handicapped,mi_diseases,education_loan,donation,sb_interest,permanent_exemption,other_deductions,V_val;
		
		
	ELSIF p_section_type='Deductions under Chapter VI (sec 80C)' THEN
		select max(deduction_limit) into limit_value from tds_taxdeductiontypes where sectiontypes=p_section_type group by sectiontypes;
		select sum(etl.amount) into produced_val FROM "employee_taxdeduction_header" eth
		INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
		WHERE "employee_id" = p_emp_id 
		and etl.section_id=p_section_type;
		
		
		IF coalesce(produced_val,0)<coalesce(limit_value,0) THEN 
			deduction_80c:=coalesce(produced_val,0);
		ELSE 
			deduction_80c:=coalesce(limit_value,0);
		END IF;
		V_val:=coalesce(deduction_80c,0);
		RAISE NOTICE 'deduction_80c: %,V_val : %',deduction_80c,V_val;
		
	ELSIF p_section_type='Deductions under Chapter VI (sec 80CCD)' THEN
		
		select id,deduction_limit into tax_id,limit_value from tds_taxdeductiontypes where sectiontypes=p_section_type and deduction_desc='National Pension scheme - Employee Contribution (sec 80CCD(1))' ;
		
		select  case when etl.amount<coalesce(limit_value,0) then etl.amount else limit_value end into deduction_80d FROM "employee_taxdeduction_header" eth
		INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines )
		WHERE "employee_id" = p_emp_id 
		and etl.deduction_desc=tax_id;
		
			
		V_val:=coalesce(deduction_80d,0);
		RAISE NOTICE 'deduction_80d: %,V_val : %',coalesce(deduction_80d,0),V_val;
	END IF;
	
	
	
		
END LOOP;

--V_val=hra_excemtion_val+t_excemption+gt_exemption+mi_exemption+lta_exemption;
--RAISE NOTICE 'empid: %, sec_type : %',p_emp_id,p_section_type;
/*select
sum(case when etl.amount<ttds.deduction_limit THEN etl.amount else ttds.deduction_limit end) tds_value into V_val
from employee_taxdeduction_header eth
INNER JOIN employee_taxlines etl on (eth.id=etl.employee_sectionlines)
INNER JOIN  tds_taxdeductiontypes ttds  ON (etl.section_id=ttds.sectiontypes and  etl.deduction_desc=ttds.id)
where eth.employee_id=p_emp_id AND ttds.sectiontypes=p_section_type
group by eth.id;
*/
RAISE NOTICE 'Return val:  %',coalesce(V_val,0);
RETURN coalesce(V_val,0);

--end_time:=CLOCK_TIMESTAMP();
--age_value:=end_time-start_time;
--	RETURN age_value;
	
	exception 
    when others then
        RAISE INFO 'Error Name:%',SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
        return V_val;
END;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.tds_deduction_val(integer, integer, text)
  OWNER TO odoo;
