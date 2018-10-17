
CREATE OR REPLACE FUNCTION public.pending_timesheet_v(
    p_date_from date,
    p_date_to date)
  RETURNS void AS
$BODY$
   BEGIN
 
	Truncate table pending_timesheet_rp;

	insert into pending_timesheet_rp(emp_id, employee, day, work_email, manager_name)
	select emp_id, employee, day, work_email, manager_name from pending_timesheet (p_date_from, p_date_to);
	END;
	
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
  
CREATE OR REPLACE FUNCTION public.pending_timesheet(
    IN p_date_from date,
    IN p_date_to date)
  RETURNS TABLE(emp_id character varying, employee character varying, day Date, work_email character varying, manager_name character varying) AS
$BODY$
DECLARE
   BEGIN
   RETURN query   
   
select b.emp_id, b.employee, a.t1date as day, b.work_email, b.manager_name from 
(select t2.empid, t2.t1date ,aal.date from 
(
select he.id empid, t1.date as t1date from hr_employee he
cross join (
select date::date
from generate_series(p_date_from, p_date_to ,interval '1 day') as t(date)
) t1 
where he.active='t' --and he.id<1000

) t2 left join account_analytic_line aal on (aal.employee_id=t2.empid and t2.t1date=aal.date)
group by t2.empid,t2.t1date,aal.date having aal.date IS NULL
order by t2.empid)a,
(
select emp.id, emp.emp_id, emp.name as employee ,emp.work_email, mgr.name as manager_name  from hr_employee emp, hr_employee mgr where emp.parent_id=mgr.id and Emp.active=true )b
where b.id=a.empid and to_char(a.t1date,'Day') not in ('Saturday ', 'Sunday   ') order by b.emp_id;
END;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
