-- Function: public.insert_same_data_with_batch_t1(text, text, date, date, boolean)

-- DROP FUNCTION public.insert_same_data_with_batch_t1(text, text, date, date, boolean);

CREATE OR REPLACE FUNCTION public.insert_same_data_with_batch_t1(
    p_tid text,
    p_fid text,
    p_fromdt date,
    p_todt date,
    p_clrdata boolean)
  RETURNS interval AS
$BODY$

DECLARE
cnt INT default 0;
inid text DEFAULT NULL;
dtst date;
dted date;
DECLARE start_time TIME ;
DECLARE end_time TIME ;
DECLARE age_value interval ;

begin
start_time:=CLOCK_TIMESTAMP();
p_clrdata:=COALESCE(p_clrdata, FALSE);
    RAISE NOTICE 'in_from_runid : %,in_to_runid : %, in_fromdt : %,in_todt :% , in_bool :%',p_fid,p_tid,p_fromdt,p_todt,p_clrdata;
	--select to_date(in_fromdt),to_date(in_todt) into dtst,dted ;   
--RAISE NOTICE 'in_runid1 : %, in_fromdt1 : %,in_todt1 :%',in_name,dtst,dted;
	/*select t2.name into inid
	from public.hr_payslip_run t1
	INNER JOIN public.hr_payslip_batch_wizard t2 on (t1.id=t2.name)
	where t1.name=in_name limit 1;
	*/
	-- return 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
	IF p_clrdata IS TRUE AND p_tid=p_fid THEN
		update hr_payslip set date_from=p_fromdt,date_to=p_todt where payslip_run_id=p_tid::int ;
		GET DIAGNOSTICS cnt = ROW_COUNT;
		RAISE NOTICE '% Records update in (hr_payslip) ',cnt;
	ELSIF p_clrdata IS TRUE AND p_tid!=p_fid THEN
		delete from hr_payslip where payslip_run_id=p_tid::int ;
		RAISE NOTICE 'existing data deleted  ';
		insert into hr_payslip(struct_id,
	name,
	"number",
	employee_id,
	date_from,
	date_to,
	state,
	company_id,
	paid,
	note,
	contract_id,
	credit_note,
	payslip_run_id,
	create_uid,
	create_date,
	write_uid,
	write_date,
	advice_id,
	date,
	journal_id,
	move_id)
	select struct_id,
	name,
	"number",
	employee_id,
	p_fromdt,
	p_todt,
	state,
	company_id,
	paid,
	note,
	contract_id,
	credit_note,
	p_tid::int,
	create_uid,
	create_date,
	write_uid,
	write_date,
	advice_id,
	date,
	journal_id,
	move_id
	from hr_payslip where payslip_run_id=p_fid::int;
		GET DIAGNOSTICS cnt = ROW_COUNT;
		RAISE NOTICE '% Records inserted into(hr_payslip)T ',cnt;
	ELSE
  	insert into hr_payslip(struct_id,
	name,
	"number",
	employee_id,
	date_from,
	date_to,
	state,
	company_id,
	paid,
	note,
	contract_id,
	credit_note,
	payslip_run_id,
	create_uid,
	create_date,
	write_uid,
	write_date,
	advice_id,
	date,
	journal_id,
	move_id)
	select struct_id,
	name,
	"number",
	employee_id,
	p_fromdt,
	p_todt,
	state,
	company_id,
	paid,
	note,
	contract_id,
	credit_note,
	p_tid::int,
	create_uid,
	create_date,
	write_uid,
	write_date,
	advice_id,
	date,
	journal_id,
	move_id
	from hr_payslip where payslip_run_id=p_fid::int;
		GET DIAGNOSTICS cnt = ROW_COUNT;
		RAISE NOTICE '% Records inserted into(hr_payslip)F ',cnt;
	END IF;
--END IF;

--update hr_payslip set date_from=dtst,date_to=dted where 
--RETURN NULL;
/*exception 
    when others then
        RAISE INFO 'Error Name:%',SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
	RETURN SQLERRM;*/
	--return NULL;
	--return query select number,employee_id,name,in_fromdt,in_todt from hr_payslip where payslip_run_id=in_tname::int and date_from=in_fromdt and date_to=in_todt group by employee_id,name,number order by employee_id;
end_time:=CLOCK_TIMESTAMP();
age_value:=end_time-start_time;
	RETURN age_value;
	
	exception 
    when others then
        RAISE INFO 'Error Name:%',SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
        return age_value;
END;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.insert_same_data_with_batch_t1(text, text, date, date, boolean)
  OWNER TO odoo;
