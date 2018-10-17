-- Function: public.pay_income_tax_cal(integer)

-- DROP FUNCTION public.pay_income_tax_cal(integer);

CREATE OR REPLACE FUNCTION public.pay_income_tax_cal(p_id integer)
  RETURNS numeric AS
$BODY$

 
declare
l1_slab integer;
l2_slab integer;
l3_slab integer ;
v_sal decimal :=0;
tax numeric := 0 ;
v_t3  decimal ;
v_t2  decimal;
v_t1 decimal;
v_sum_pt  numeric default 0;
v_employee_id integer;
v_pt_count  integer;
v_pt_max integer;
t_count integer default 12;
v_max_date date;
 v_sal_sum integer;
 v_sal_count integer;
 v_sal_max_date date;
 t_sal_count integer default 12;
 v_sal_max integer;
 v_excem1 numeric;
 v_excem2 numeric;
 v_excem3 numeric;
 v_excem4 numeric;
 v_excem5 numeric;
 v_excem6 numeric;
 v_nps_val numeric;
 v_nps_max numeric;
 v_nps_cnt integer;
 v_nps_sum numeric;
 t_nps_cnt integer default 12;
 v_nps_date date;
 v_year integer;
 fyear_start date;
begin

/* SELECT TOTAL INTO v_pt FROM HR_PAYSLIP_LINE WHERE NAME LIKE 'Professional Tax%' AND CONTRACT_ID IN 
(SELECT ID FROM HR_CONTRACT WHERE id =  p_id); */ 
-- insert into test_message values(1,v_pt); 

 select employee_id  into v_employee_id
 from 	hr_contract hc  ,
	hr_payroll_structure hps, 
	hr_structure_salary_rule_rel hsr,
	hr_salary_rule hsru
where  hc.id = p_id 
and hc.struct_id = hps.id  
and hps.id = hsr.struct_id 
and hsr.rule_id = hsru.id 
and hsru.name = 'Tax Deducted at Source'  ;

select max(date_to) into  v_sal_max_date
 from 	hr_payslip  hp ,
	hr_employee he ,
	hr_payslip_line hpl
where hp.employee_id = he.id 
and hpl.slip_id = hp.id
and hpl.name = 'Gross' 
and he.id = v_employee_id 
group by he.id ;

RAISE NOTICE 'v_sal_max_date : %',v_sal_max_date;
v_year:=date_part('year',v_sal_max_date);
fyear_start:=v_year||'-04-01';
RAISE NOTICE 'v_year : %,fyear_start : %',v_year,fyear_start;

-- for salary 
 select sum(amount),count(he.id ),max(date_to) into  v_sal_sum,v_sal_count,v_sal_max_date
 from 	hr_payslip  hp ,
	hr_employee he ,
	hr_payslip_line hpl
where hp.employee_id = he.id 
and hpl.slip_id = hp.id
and hpl.name = 'Gross' 
and he.id = v_employee_id 
and date_to>=fyear_start
group by he.id ;

RAISE NOTICE 'v_sal_sum : %,v_sal_count : %,v_sal_max_date : %',v_sal_sum,v_sal_count,v_sal_max_date;
select amount into v_sal_max 
from hr_payslip  hp ,hr_payslip_line hpl
where hpl.slip_id = hp.id
and hpl.name = 'Gross' 
and hp.employee_id = v_employee_id
and date_to = v_sal_max_date;
RAISE NOTICE 'current_month_sal : %',v_sal_max;


t_sal_count := t_sal_count - v_sal_count;

v_sal := v_sal_sum + (v_sal_max *  t_sal_count) ;
RAISE NOTICE 'Before excemptions, Gross Value: %  ',v_sal;

 select sum(amount*0.1),count(he.id ),max(date_to) into  v_nps_val,v_nps_cnt,v_nps_date
 from 	hr_payslip  hp ,
	hr_employee he ,
	hr_payslip_line hpl
where hp.employee_id = he.id 
and hpl.slip_id = hp.id
and hpl.name = 'Basic Salary' 
and he.id = v_employee_id 
and date_to>=fyear_start
group by he.id ;
RAISE NOTICE 'v_nps_val : %,v_nps_cnt : %,v_nps_date : %',v_nps_val,v_nps_cnt,v_nps_date;

select amount*0.1 into v_nps_max 
from hr_payslip  hp ,hr_payslip_line hpl
where hpl.slip_id = hp.id
and hpl.name = 'Basic Salary' 
and hp.employee_id = v_employee_id
and date_to = v_nps_date;

RAISE NOTICE 'v_nps_max : %,t_nps_cnt : %',v_nps_max,t_nps_cnt;

t_nps_cnt=t_nps_cnt-v_nps_cnt;
RAISE NOTICE 't_nps_cnt : %',t_nps_cnt;
v_nps_sum :=v_nps_val + (v_nps_max*t_nps_cnt) ;
RAISE NOTICE 'nps_value : %',v_nps_sum;
v_sal:=v_sal+v_nps_sum;
RAISE NOTICE 'After adding nps(%), Gross Value: %  ',v_nps_sum,v_sal;

select public.tds_deduction_val(p_id,v_employee_id,'Exemptions under section 10 & 17') into v_excem1;
select public.tds_deduction_val(p_id,v_employee_id,'Home Loan Interest and property Income/Loss') into v_excem2;
select public.tds_deduction_val(p_id,v_employee_id,'Other income') into v_excem3;
select public.tds_deduction_val(p_id,v_employee_id,'Deductions under Chapter VI-A') into v_excem4;
select public.tds_deduction_val(p_id,v_employee_id,'Deductions under Chapter VI (sec 80C)') into v_excem5;
select public.tds_deduction_val(p_id,v_employee_id,'Deductions under Chapter VI (sec 80CCD)') into v_excem6;
--RAISE NOTICE 'v_sal: %, v_excem1 : %,v_excem2: %,v_excem3: %, v_excem4: %, v_excem5 : %,v_excem6: % ,:After  excemptions, Gross Value: %  ',v_sal,v_excem1,v_excem2,v_excem3,v_excem4,v_excem5,v_excem6,v_sal;

v_sal:=v_sal-v_excem1-v_excem2+v_excem3-v_excem4-v_excem5-v_excem6;
--RAISE NOTICE 'v_sal: %, v_excem1 : %,v_excem2: %,v_excem3: %, v_excem4: %, v_excem5 : %,v_excem6: % ,:After  excemptions, Gross Value: %  ',v_sal,v_excem1,v_excem2,v_excem3,v_excem4,v_excem5,v_excem6,v_sal;
RAISE NOTICE 'After excemptions Gross salary: %',v_sal;

-- Professional_tax  
 select sum(amount),count(he.id ),max(date_to) into  v_sum_pt,v_pt_count,v_max_date 
 from 	hr_payslip  hp ,
	hr_employee he ,
	hr_payslip_line hpl
where hp.employee_id = he.id 
and hpl.slip_id = hp.id
and hpl.name = 'Professional Tax' 
and he.id = v_employee_id 
and date_to>=fyear_start
group by he.id 
;
RAISE NOTICE 'v_sum_pt : %,v_pt_count : %,v_max_date : %',v_sum_pt,v_pt_count,v_max_date;
select amount into v_pt_max 
from hr_payslip  hp ,hr_payslip_line hpl
where hpl.slip_id = hp.id
and hpl.name = 'Professional Tax' 
and hp.employee_id = v_employee_id
and date_to = v_max_date;
 
RAISE NOTICE 'v_pt_max : %',v_pt_max;
t_count := t_count - COALESCE(v_pt_count,0);

select max into l1_slab from tax_slab where slab_id = 1 ;
select max into l2_slab from tax_slab where slab_id = 2;
select max into l3_slab from tax_slab where slab_id = 3 ;
v_sum_pt  := COALESCE(v_sum_pt ,0)	;
   --RAISE NOTICE 'After PT excemption, Gross Value: % ,v_sum_pt : %,v_pt_max :% ',v_sal,v_sum_pt,v_pt_max;
  v_sal :=  v_sal + v_sum_pt + (COALESCE(v_pt_max,0) * t_count) ;

  RAISE NOTICE 'After PT excemption, Gross Value: %  ',v_sal;

--  raise notice 'program started|| v_sal!' ,v_sal ;
   IF v_sal > l3_slab
   THEN
       v_t3 := (v_sal-l3_slab)*0.3  ;
	   v_t2 := (l2_slab) * 0.2 ;
	   v_t1:= (l1_slab)*0.05 ;
	   tax := v_t3+v_t2+v_t1;
	elsif v_sal > l2_slab 
	then 
	 v_t2 := (v_sal-l2_slab) * 0.2 ;
	   v_t1:= (l1_slab)*0.05 ;
		   tax := v_t2+v_t1;
	elsif v_sal > l1_slab 
	then 
	   v_t1:= (v_sal-l1_slab)*0.05 ;
		   tax := v_t1;
	elsif v_sal < l1_slab  
	then tax := 0 ; 
	
  END IF;
  tax:=tax+(tax*0.04);
  
  
  RAISE NOTICE 'hr_contract updating values : % ,% ,%, % ,%, 80c_80D : %',round((tax/12),0),v_excem1,v_excem2,v_excem3,v_excem4,v_excem5+v_excem6;
  update hr_contract  set tds= round((tax/12),0),
	exemptions_undersection=v_excem1,
	income_chargeable_houseproperty=v_excem2,
	income_chargeable_otherhead_sources=v_excem3,
	deductions_underchapter_6a=v_excem4,
	deductions_under80c_80ccd=v_excem5+v_excem6
	where id = p_id   ;
   return round((tax/12),0);
   end;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.pay_income_tax_cal(integer)
  OWNER TO postgres;
