-- Function: public.calculate_components(integer)

-- DROP FUNCTION public.calculate_components(integer);

CREATE OR REPLACE FUNCTION public.calculate_components(p_cid integer)
  RETURNS text AS
$BODY$

 DECLARE cnt INT DEFAULT 0;
 DECLARE age_value interval ;
 DECLARE start_time TIME ;
 DECLARE end_time TIME ;
 DECLARE rec_hr_contract record;
 DECLARE basic numeric default 0;
 DECLARE hra numeric default 0;
 DECLARE c_allowance numeric default 0;
 DECLARE epf numeric default 0;
 DECLARE erpf numeric default 0;
 DECLARE gdv numeric default 0;
 DECLARE p_bill numeric default 0;
 DECLARE lta_val numeric default 0;
 DECLARE t_bill numeric default 0;
 DECLARE f_pay numeric default 0;
 DECLARE gsal numeric default 0;
 DECLARE mv numeric default 0;
 DECLARE mi numeric default 0;
 DECLARE empr_esi numeric default 0;
 DECLARE emp_esi numeric default 0;
 DECLARE sp_allowance numeric default 0;
 DECLARE in_nontaxable_reimbursment numeric default 0;
 DECLARE dsal numeric default 0;
 DECLARE pt_val numeric default 0;
 DECLARE nps_val numeric default 0;
 DECLARE nt_reim record;
 
 
 
BEGIN
start_time:=CLOCK_TIMESTAMP();
FOR  rec_hr_contract IN SELECT cost_to_company,employeepf_exempt,employerspf_exempt,gratuity_exempt,petrolbill_exempt,lta_exempt,telephonebill_exempt,hra_exempt,flexiblepay_exempt,medicalinsurance_exempt,conveyanceallowance_exempt,employersesi_exempt,mealvouchers_exempt,struct_id,CASE WHEN coalesce(char_length((trim(grade))),0)>0 THEN grade ELSE '0' END grade,employeeesi_exempt,driver_salary_exempt,professional_tax_exempt FROM "hr_contract" hc,"hr_employee" he WHERE (employee_id=he.id) and hc."id" = p_cid

LOOP
gsal:=rec_hr_contract.cost_to_company/12;
/*
IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='GT'
) THEN*/
	IF rec_hr_contract.gratuity_exempt IS FALSE THEN 
		gdv:=0;
	ELSE
		gdv:=((gsal/26)*15);
	END IF;
/*ELSE
gdv:=0;
END IF;	
*/
IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='BASIC'
) THEN
basic:=gsal*0.5;
ELSE
basic:=0;
END IF;

	
IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='HRAMN'
) THEN
	IF rec_hr_contract.hra_exempt IS FALSE THEN 
		hra:=0;
	ELSE
		hra:=basic*0.4;
	END IF;
ELSE
hra:=0;
END IF;

IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='CA'
) THEN
	IF rec_hr_contract.conveyanceallowance_exempt IS FALSE THEN 
		c_allowance:=0;
	ELSE
		c_allowance:=1800;
	END IF;
ELSE
c_allowance:=0;
END IF;

	
IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='FP'
) THEN		
	IF rec_hr_contract.flexiblepay_exempt IS FALSE THEN 
		f_pay:=0;
	ELSE
		f_pay:=(rec_hr_contract.cost_to_company*0.1)/12;
	END IF;
ELSE
f_pay:=0;
END IF;		

IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='EPMF'
) THEN
	IF rec_hr_contract.employeepf_exempt IS FALSE THEN 
		epf:=0;
	ELSE
		epf:=(basic*0.12);
	END IF;
ELSE
epf:=0;
END IF;	

/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='EPF'
) THEN*/
	IF rec_hr_contract.employerspf_exempt IS FALSE THEN 
		erpf:=0;
	ELSE
		erpf:=ROUND((basic*0.12),0);
	END IF;
/*ELSE
erpf:=0;
END IF;	
*/	
IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='CMT'
) THEN		
	IF rec_hr_contract.medicalinsurance_exempt IS FALSE THEN 
		mi:=0;
	ELSE
		mi:=1000;
	END IF;
ELSE
mi:=0;
END IF;	

RAISE NOTICE 'grade : %,',rec_hr_contract.grade;
IF (rec_hr_contract.grade::int IS NOT NULL )
THEN 
FOR nt_reim IN select *from non_taxable_reimbursments where job_grade_id=rec_hr_contract.grade::int
LOOP
		RAISE NOTICE 'grade : %,fuel : %, lta : %,driver : %,t_bill : %,meal_coupons : %',rec_hr_contract.grade,nt_reim.fuel,nt_reim.lta,nt_reim.driver,nt_reim.telephone_bill,nt_reim.meal_coupons;
	--lta,fuel,driver,telephone_bill,meal_coupons into 
	/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
	INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
	where struct_id=rec_hr_contract.struct_id and hsr.code='MV'
	) THEN		*/
		IF rec_hr_contract.mealvouchers_exempt IS FALSE THEN 
			mv:=0;
		ELSE
			mv:=nt_reim.meal_coupons;
		END IF;
	/*ELSE
	mv:=0;
	END IF;		
	*/
	/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
	INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
	where struct_id=rec_hr_contract.struct_id and hsr.code='LT'
	) THEN	*/
		IF rec_hr_contract.lta_exempt IS FALSE THEN 
			lta_val:=0;
		ELSE
			lta_val:=nt_reim.lta;
		END IF;
	/*ELSE
	lta_val:=0;
	END IF;		
	*/	
		
	/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
	INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
	where struct_id=rec_hr_contract.struct_id and hsr.code='PB'
	) THEN*/
		IF rec_hr_contract.petrolbill_exempt IS FALSE THEN 
			p_bill:=0;
		ELSE
			p_bill:=nt_reim.fuel;
			IF p_bill>0 THEN 
				c_allowance:=0;
			END IF;
		END IF;
	/*ELSE
	p_bill:=0;
	END IF;	
	*/	
	
	
	/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
	INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
	where struct_id=rec_hr_contract.struct_id and hsr.code='TB'
	) THEN		*/
		IF rec_hr_contract.telephonebill_exempt IS FALSE THEN 
			t_bill:=0;
		ELSE
			t_bill:=nt_reim.telephone_bill;
		END IF;
	/*ELSE
	t_bill:=0;
	END IF;		
	*/
	/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
	INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
	where struct_id=rec_hr_contract.struct_id and hsr.code='DS'
	) THEN		*/
		IF rec_hr_contract.driver_salary_exempt IS FALSE THEN 
			dsal:=0;
		ELSE
			dsal:=nt_reim.driver;
		END IF;
	/*ELSE
	t_bill:=0;
	END IF;		
	*/
END LOOP;
ELSE
mv:=0;
lta_val:=0;
p_bill:=0;
t_bill:=0;
dsal:=0;
END IF;

 
 
	/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
	INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
	where struct_id=rec_hr_contract.struct_id and hsr.code='ERESI'
	) THEN		*/
		IF gsal<=21000 THEN 
			IF rec_hr_contract.employersesi_exempt IS FALSE THEN 
				empr_esi:=0;
			ELSE
				empr_esi:=(basic+hra+c_allowance)*0.0475;
			END IF;
		ELSE 
			empr_esi:=0;
		END IF;
	/*ELSE
	empr_esi:=0;
	END IF;	
	*/
/*IF EXISTS (select hsr.name,hs.*from hr_structure_salary_rule_rel hs
INNER JOIN hr_salary_rule hsr on (hs.rule_id=hsr.id)
where struct_id=rec_hr_contract.struct_id and hsr.code='ESI'
) THEN	*/
	IF gsal<=21000 	THEN 
		IF rec_hr_contract.employeeesi_exempt IS FALSE THEN 
			emp_esi:=0;
		ELSE
			emp_esi:=(basic+hra+c_allowance)*0.0175;
		END IF;
	ELSE 
		emp_esi:=0;
	END IF;
/*ELSE
emp_esi:=0;
END IF;	*/
	/*IF rec_hr_contract.professional_tax_exempt IS FALSE THEN 
		pt_val:=0;
	ELSE */
		IF gsal>20000 THEN 
			pt_val:=200;
		ELSIF gsal<=20000 and gsal> 15000 THEN 
			pt_val:=150;
		ELSE 
			pt_val:=0;	
		END IF;
		
	/*END  IF;*/
	
	in_nontaxable_reimbursment:=(((lta_val+mv+p_bill+t_bill+dsal)/12)+mi);
	sp_allowance=gsal-basic-hra-c_allowance-f_pay-in_nontaxable_reimbursment-erpf-empr_esi-gdv/12;
	RAISE NOTICE 'Id: %,gsal: %,basic : %,hra: %,c_allowance: %,epf: %,erpf: %,gratuity: %,p_bill: %,lta: %,mv : %,t_bill: %,driver_sal : %,f_pay: %,mi: %,wage: %,non_tx : %,s_all: %,empr_esi : %',p_cid,gsal,basic,hra,c_allowance,epf,erpf,ROUND((gdv/12),0),p_bill/12,lta_val/12,mv/12,t_bill/12,dsal/12,f_pay,mi,ROUND(basic,0),ROUND(in_nontaxable_reimbursment,0),ROUND(sp_allowance,0),ROUND(empr_esi,0);
	gsal=basic+hra+c_allowance+f_pay+sp_allowance+in_nontaxable_reimbursment;
	
	--nps_val:=(basic)*0.1;
	RAISE NOTICE 'Gross Salary : % ',gsal;
END LOOP;

UPDATE hr_contract set conveyance_allowance=c_allowance,
employee_pf=ROUND(epf,0),
employers_pf=ROUND(erpf,0),
gratuity=ROUND((gdv/12),0),
petrol_bill=p_bill/12,
lta=ROUND(lta_val/12,0),
telephone_bill=ROUND(t_bill/12,0),
flexible_pay=f_pay,
medical_insurance=mi,
meal_vouchers=ROUND(mv/12,0),
special_allowance=ROUND(sp_allowance,0),
wage=ROUND(basic,0),
gross_salary=ROUND(gsal,0),--+ROUND(nps_val,0)
driver_salary=ROUND(dsal/12,0),
nontaxable_reimbursment=in_nontaxable_reimbursment,
professional_tax=ROUND(pt_val,0),
employee_esi=ROUND(emp_esi,0),
employers_esi=ROUND(empr_esi,0)

where "id" = p_cid ;
GET DIAGNOSTICS cnt = ROW_COUNT;
RAISE NOTICE '% Records effected in hr_contract',cnt;

end_time:=CLOCK_TIMESTAMP();
age_value:=end_time-start_time;
	RETURN age_value;
	
	exception 
    when others then
        RAISE INFO 'Error Name:%',SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
        return 'Error '||SQLSTATE||':'||SQLERRM;
END

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.calculate_components(integer)
  OWNER TO odoo;
