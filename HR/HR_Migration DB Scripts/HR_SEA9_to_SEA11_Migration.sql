-- FUNCTION: public.fdw_connect_setup(text, text, text, text, text, text, text)

-- DROP FUNCTION public.fdw_connect_setup(text, text, text, text, text, text, text);

CREATE OR REPLACE FUNCTION public.fdw_connect_setup(
	inhost text,
	infport text,
	infdb text,
	infuser text,
	infpwd text,
	infschema text,
	inlschema text)
    RETURNS interval
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
AS $BODY$

 DECLARE age_value interval ;
 DECLARE start_time TIME ;
 DECLARE end_time TIME ;
BEGIN

start_time:=CLOCK_TIMESTAMP();
	create schema odoo9;
    DROP EXTENSION  IF EXISTS  postgres_fdw CASCADE;
	CREATE EXTENSION postgres_fdw; 
	RAISE NOTICE ' Extension postgres_fdw created ';
	
    EXECUTE 'CREATE SERVER Odoo9_server
	FOREIGN DATA WRAPPER postgres_fdw
	OPTIONS (host ' ||quote_literal(inhost)||',port '||quote_literal(infport)||', dbname '||quote_literal(infdb)||')'
    USING inhost, infport,infdb;
    RAISE NOTICE ' Server Created Successfully ip: % ,port: % ,db: % ',inhost, infport,infdb;
	
    EXECUTE 'CREATE USER MAPPING FOR CURRENT_USER
	SERVER Odoo9_server
	OPTIONS (user '||quote_literal(infuser)||', password '||quote_literal(infpwd)||')'
	USING infuser, infpwd;
    RAISE NOTICE ' User Mapping Created Successfully user: % ,pwd: % ',infuser, infpwd;
	
	EXECUTE 'IMPORT FOREIGN SCHEMA '||infschema||'
	FROM SERVER Odoo9_server
	INTO '||inlschema
	USING infschema, inlschema;
	RAISE NOTICE ' Tables imported into : % from schema : % ',inlschema, infschema;
	
end_time:=CLOCK_TIMESTAMP();
age_value:=end_time-start_time;
	RETURN age_value;
END

$BODY$;


	-- select public.fdw_connect_setup('192.168.0.181', '5432', 'odoo9_14062018', 'postgres', 'root123', 'public', 'odoo9')
	------------------------------------------------------------------------------
-- Function: public.emp_module_function()



-- DROP FUNCTION public.emp_module_function();



CREATE OR REPLACE FUNCTION public.emp_module_function()

  RETURNS interval AS

$BODY$



 DECLARE cnt INT DEFAULT 0;

 DECLARE max_id INT DEFAULT 0; 

 DECLARE age_value interval ;

 DECLARE start_time TIME ;

 DECLARE end_time TIME ;

BEGIN

start_time:=CLOCK_TIMESTAMP();





BEGIN

ALTER TABLE public.mail_alias DISABLE TRIGGER ALL;



	INSERT INTO public.mail_alias ( id,

			alias_name ,

			alias_model_id,

			alias_user_id,

			alias_defaults,

			alias_force_thread_id ,

			

			alias_parent_model_id ,

			alias_parent_thread_id,

			alias_contact,

			create_uid ,

			create_date  ,

			write_uid,

			write_date 

			)

		

		SELECT   id,

			alias_name ,

			alias_model_id,

			alias_user_id,

			alias_defaults,

			alias_force_thread_id ,

			

			alias_parent_model_id ,

			alias_parent_thread_id,

			alias_contact,

			create_uid ,

			create_date  ,

			write_uid,

			write_date 

			

	FROM odoo9.mail_alias  ON CONFLICT(id) DO update set alias_name=excluded.alias_name,alias_parent_model_id=excluded.alias_parent_model_id,alias_defaults=excluded.alias_defaults,alias_model_id=excluded.alias_model_id ,alias_parent_thread_id=excluded.alias_parent_thread_id,alias_force_thread_id=excluded.alias_force_thread_id;

	

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(mail_alias) odoo11 server from odoo9',cnt;

ALTER TABLE public.mail_alias ENABLE TRIGGER ALL; 

END;





ALTER SEQUENCE public.mail_alias_id_seq RESTART WITH 1;



ALTER TABLE public.res_users DISABLE TRIGGER ALL;



	INSERT INTO public.res_users (id 

									,active

									,login 

									,password

									,company_id 

									,partner_id 

									,create_date 

									,create_uid

									,share

									,write_uid

									,write_date

									,signature

									,action_id

									,password_crypt

									,alias_id

									,notification_type
									,sale_team_id

   )

										

							  SELECT id 

									,'t' active

									,login 

									,password

									,company_id 

									,partner_id 

									,create_date 

									,create_uid

									,share

									,write_uid

									,write_date

									,signature

									,action_id

									,password_crypt

									,alias_id  

									,'email' notification_type  
									,1 saleteamid

	FROM odoo9.res_users  ON CONFLICT(id) DO UPDATE set login=excluded.login||' ',partner_id=excluded.partner_id,signature=excluded.signature,write_uid=excluded.write_uid,alias_id=excluded.alias_id; --NOTHING ;--where id>10;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_users) odoo11 server from odoo9',cnt;

	

ALTER TABLE public.res_users ENABLE TRIGGER ALL; 



update res_users set login='joshua.tippanna@sailotech.com' where id=1;



ALTER TABLE public.hr_department DISABLE TRIGGER ALL;



	INSERT INTO public.hr_department ( id,

			create_date ,

			name,

			complete_name,

			active,

			create_uid ,

			color ,

			message_last_post,

			company_id,

			write_uid ,

			note  ,

			parent_id,

			manager_id ,

			write_date)

		

		SELECT   id,

			create_date ,

			name,

			name,

			'true',

			create_uid ,

			color ,

			message_last_post,

			company_id,

			write_uid ,

			note  ,

			parent_id,

			manager_id ,

			write_date

	FROM odoo9.hr_department    ON CONFLICT(id) DO NOTHING ;--where id>10;



	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(hr_department) odoo11 server from odoo9',cnt;

ALTER TABLE public.hr_department ENABLE TRIGGER ALL; 







ALTER TABLE public.hr_employee DISABLE TRIGGER ALL;

	INSERT INTO public.hr_employee ( id 

									,address_id

									,create_date

									,coach_id

									,resource_id

									,color

									,message_last_post

									,marital

									,identification_id

									,bank_account_id

									,job_id

									,work_phone

									,country_id

									,parent_id

									,department_id

									,mobile_phone

									,create_uid

									,birthday

									,write_date

									,sinid

									,write_uid

									,work_email

									,work_location

									,gender

									,ssnid

									,address_home_id

									,passport_id 

									,notes

									,grade 

									,dod 

									,name

									,pancard_no

									,doj

									,emp_id

									,active)

			

		SELECT   id 

		        ,address_id

		        ,create_date

		        ,coach_id

		        ,resource_id

		        ,color

		        ,message_last_post

		        ,marital

		        ,identification_id

		        ,bank_account_id

		        ,job_id

		        ,work_phone

		        ,country_id

		        ,parent_id

		        ,department_id

		        ,mobile_phone

		        ,create_uid

		        ,birthday

		        ,write_date

		        ,sinid

		        ,write_uid

		        ,work_email

		        ,work_location

		        ,gender

		        ,ssnid

		        ,address_home_id

		        ,passport_id 

		        ,notes

		        ,grade 

		        ,dod 

				,name_related

				,x_pancard_no

				,x_date_of_joining

				,x_emp_id

				,'t'

		FROM odoo9.hr_employee ON CONFLICT(id) DO NOTHING;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(hr_employee) odoo11 server from odoo9',cnt;

ALTER TABLE public.hr_employee ENABLE TRIGGER ALL;







ALTER TABLE public.resource_resource DISABLE TRIGGER ALL;

	insert into public.resource_resource( id 

										 ,create_uid

										 ,time_efficiency 

										 ,user_id 

										 ,name 

										 ,company_id

										 ,write_uid

										 ,write_date

										 ,calendar_id 

										 ,active

										 ,create_date

										 ,resource_type)

		select  id 

				,create_uid

				,time_efficiency 

				,user_id 

				,name 

				,company_id

				,write_uid

				,write_date

				,1 calendar_id 

				,'t' active

				,create_date

				,resource_type

	from odoo9.resource_resource   ON CONFLICT(id) DO NOTHING;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(resource_resource) odoo11 server from odoo9',cnt;

ALTER TABLE public.resource_resource ENABLE TRIGGER ALL; 







ALTER TABLE public.res_partner DISABLE TRIGGER ALL;



	INSERT INTO public.res_partner ( id 

									,name

									,company_id

									,comment

									,function 

									,create_date

									,color

									,date

									,street

									,city 

									,display_name

									,zip

									,title

									,country_id

									,parent_id

									,supplier

									,ref 

									,email

									,is_company

									,website 

									,customer 

									,street2

									,barcode

									,employee

									,credit_limit

									,write_date

									,active

									,tz 

									,write_uid 

									,lang 

									,create_uid

									,phone 

									,mobile 

									,type

									,user_id

									,vat 

									,state_id 

									,commercial_partner_id 

									,message_last_post 

									,opt_out 

									,signup_type 

									,signup_expiration 

									,signup_token 

									,last_time_entries_checked

									,debit_limit

									,calendar_last_notif_ack

									,invoice_warn)

			

		select  id 

				,name

				,company_id

				,comment

				,function 

				,create_date

				,color

				,date

				,street

				,city 

				,display_name

				,zip

				,title

				,country_id

				,parent_id

				,supplier

				,ref 

				,email

				,is_company

				,website 

				,customer 

				,street2

				,barcode

				,employee

				,credit_limit

				,write_date

				,active

				,tz 

				,write_uid 

				,lang 

				,create_uid

				,phone 

				,mobile 

				,type

				,user_id

				,vat 

				,state_id 

				,commercial_partner_id 

				,message_last_post 

				,opt_out 

				,signup_type 

				,signup_expiration 

				,signup_token 

				,last_time_entries_checked

				,debit_limit

				,calendar_last_notif_ack

				,'no-message' invoice_warn

			from odoo9.res_partner  ON CONFLICT(id) DO UPDATE set name=excluded.name,display_name=excluded.display_name,email=excluded.email,commercial_partner_id=excluded.commercial_partner_id,country_id=excluded.country_id,invoice_warn='',website=excluded.website,commercial_partner_country_id=excluded.country_id;--where id>10;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_partner) odoo11 server from odoo9',cnt;



 ALTER TABLE public.res_partner ENABLE TRIGGER ALL;

 







	

ALTER TABLE public.hr_job DISABLE TRIGGER ALL;



	INSERT INTO public.hr_job ( id

				,create_uid 

				,create_date

				,description 

				,name 

				,message_last_post 

				,company_id 

				,write_uid 

				,expected_employees 

				,state 

				,no_of_recruitment 

				,write_date

				,requirements 

				,no_of_hired_employee 

				,no_of_employee

				,department_id )

 



		SELECT  id,

				create_uid,

				create_date,

				description,

				name,

				message_last_post,

				company_id,

				write_uid,

				expected_employees,

				state,

				no_of_recruitment,

				write_date,

				requirements,

				no_of_hired_employee,

				no_of_employee,

				department_id

	FROM odoo9.hr_job   ON CONFLICT(id) DO NOTHING;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(hr_job) odoo11 server from odoo9',cnt;



ALTER TABLE public.hr_job ENABLE TRIGGER ALL; 

	



		

 

ALTER TABLE public.hr_employee_category DISABLE TRIGGER ALL;

 

	INSERT INTO public.hr_employee_category (id,

			create_uid,

			create_date,

			name,

			color,

			write_uid,

			write_date)



		SELECT id,

			create_uid,

			create_date,

			name,

			color,

			write_uid,

			write_date 

	FROM odoo9.hr_employee_category   ON CONFLICT(id) DO NOTHING;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(hr_employee_category) odoo11 server from odoo9',cnt;



ALTER TABLE public.hr_employee_category ENABLE TRIGGER ALL; 





ALTER TABLE public.res_company DISABLE TRIGGER ALL;

	insert into public.res_company(id,

				name ,

				partner_id ,

				currency_id,

				parent_id ,

				logo_web ,

				account_no ,

				email ,

				phone ,

				company_registry ,

				paperformat_id ,

				create_uid ,

				create_date,

				write_uid ,

				write_date ,

				project_time_mode_id ,

				fiscalyear_last_day ,

				fiscalyear_last_month ,

				period_lock_date ,

				fiscalyear_lock_date ,

				transfer_account_id ,

				expects_chart_of_accounts ,

				chart_template_id ,

				bank_account_code_prefix ,

				cash_account_code_prefix ,

				accounts_code_digits ,

				tax_calculation_rounding_method ,

				currency_exchange_journal_id ,

				anglo_saxon_accounting ,

				property_stock_account_input_categ_id ,

				property_stock_account_output_categ_id ,

				property_stock_valuation_account_id ,

				overdue_msg )

				

		select id,name ,

				partner_id ,

				currency_id,

				parent_id ,

				logo_web ,

				account_no ,

				email ,

				phone ,

				company_registry ,

				paperformat_id ,

				create_uid ,

				create_date,

				write_uid ,

				write_date ,

				project_time_mode_id ,

				fiscalyear_last_day ,

				fiscalyear_last_month ,

				period_lock_date ,

				fiscalyear_lock_date ,

				transfer_account_id ,

				expects_chart_of_accounts ,

				chart_template_id ,

				bank_account_code_prefix ,

				cash_account_code_prefix ,

				accounts_code_digits ,

				tax_calculation_rounding_method ,

				currency_exchange_journal_id ,

				anglo_saxon_accounting ,

				property_stock_account_input_categ_id ,

				property_stock_account_output_categ_id ,

				property_stock_valuation_account_id ,

				overdue_msg 

	from odoo9.res_company   ON CONFLICT(id) DO UPDATE SET name=excluded.name,email=excluded.email,overdue_msg=excluded.overdue_msg,logo_web=excluded.logo_web;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_company) odoo11 server from odoo9',cnt;

	

ALTER TABLE public.res_company ENABLE TRIGGER ALL;	







ALTER TABLE public.account_analytic_line DISABLE TRIGGER ALL;

	insert into public.account_analytic_line(

				id ,

				name ,

				date ,

				amount,

				unit_amount ,

				account_id ,

				partner_id ,

				user_id ,

				company_id ,

				create_uid ,

				create_date,

				write_uid ,

				write_date ,

				task_id ,

				product_uom_id ,

				product_id ,

				general_account_id ,

				move_id ,

				code,

				ref ,

				currency_id ,

				amount_currency

				,project_id

				,employee_id)

				

		select aal.id ,

				aal.name ,

				aal.date ,

				aal.amount,

				aal.unit_amount ,

				aal.account_id ,

				aal.partner_id ,

				case when aal.user_id IS NULL then 1 else aal.user_id end user_id1,

				aal.company_id ,

				aal.create_uid ,

				aal.create_date,

				aal.write_uid ,

				aal.write_date ,

				aal.task_id ,

				aal.product_uom_id ,

				aal.product_id ,

				aal.general_account_id ,

				aal.move_id ,

				aal.code,

				aal.ref ,

				aal.currency_id ,

				aal.amount_currency

				,pp.id

				,case when htss.employee_id IS NULL then 1 else htss.employee_id end emp_id

	from odoo9.account_analytic_line aal 

        LEFT JOIN odoo9.res_users ru on (aal.partner_id=ru.partner_id)

        LEFT JOIN odoo9.resource_resource rr on (rr.user_id=ru.id)  

		LEFT JOIN odoo9.project_project pp on (aal.account_id=pp.analytic_account_id)
		LEFT JOIN odoo9.hr_timesheet_sheet_sheet htss on (aal.sheet_id=htss.id);

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(account_analytic_line) odoo11 server from odoo9',cnt;

	

ALTER TABLE public.account_analytic_line ENABLE TRIGGER ALL;



ALTER TABLE public.account_analytic_account DISABLE TRIGGER ALL;

INSERT INTO public.account_analytic_account(id

											,name

											,code

											,active

											,company_id

											,partner_id

											,message_last_post

											,create_uid

											,create_date

											,write_uid

											,write_date)

									select id

										  ,name

										  ,code

										  ,'t'

										  ,company_id

										  ,partner_id

										  ,message_last_post

										  ,create_uid

										  ,create_date

										  ,write_uid

										  ,write_date

									from odoo9.account_analytic_account    ON CONFLICT(id) DO UPDATE set name=excluded.name,partner_id=excluded.partner_id,write_uid=excluded.write_uid ;--where id>3;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(account_analytic_account) odoo11 server from odoo9',cnt;												



ALTER TABLE public.account_analytic_account ENABLE TRIGGER ALL;



ALTER TABLE public.res_config_settings DISABLE TRIGGER ALL;

	insert into public.res_config_settings(	id,

				create_uid,

				create_date,

				write_date,

				write_uid,

				company_id )

	

		select id,

				create_uid,

				create_date,

				write_date,

				write_uid,

				1 company_id 

	from odoo9.res_config_settings   ON CONFLICT(id) DO NOTHING;
	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_config_settings) odoo11 server from odoo9',cnt;	
	
ALTER TABLE public.res_config_settings ENABLE TRIGGER ALL;



ALTER TABLE public.calendar_event DISABLE TRIGGER ALL;

	insert into public.calendar_event(	id
,allday
,create_date
,display_start
,recurrency
,start_datetime
,write_uid
,duration
,month_by
,rrule
,final_date
,create_uid
,user_id
,tu
,message_last_post
,week_list
,day
,start
,state
,location
,th
,start_date
,recurrent_id_date
,description
,stop_date
,stop
,stop_datetime
,fr
,write_date
,active
,byday
,count
,end_type
,name
,we
,mo
,interval
,su
,recurrent_id
,sa
,rrule_type
,show_as
,opportunity_id )

	select id
,allday
,create_date
,display_start
,recurrency
,start_datetime
,write_uid
,duration
,month_by
,rrule
,final_date
,create_uid
,user_id
,tu
,message_last_post
,week_list
,day
,start
,state
,location
,th
,start_date
,recurrent_id_date
,description
,stop_date
,stop
,stop_datetime
,fr
,write_date
,active
,byday
,count
,end_type
,name
,we
,mo
,interval
,su
,recurrent_id
,sa
,rrule_type
,show_as
,opportunity_id

	from odoo9.calendar_event   ON CONFLICT(id) DO NOTHING;
	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(calendar_event) odoo11 server from odoo9',cnt;	
	
ALTER TABLE public.calendar_event ENABLE TRIGGER ALL;



ALTER TABLE public.calendar_contacts DISABLE TRIGGER ALL;

	insert into public.calendar_contacts(	id
,create_uid
,create_date
,write_uid
,write_date
,active
,user_id
,partner_id
 )

	select id
,CASE WHEN create_uid IS NULL THEN 1 else create_uid end cuid
,create_date
,CASE WHEN write_uid  IS NULL THEN 1 else write_uid end wuid
,write_date
,active
,CASE WHEN  user_id   IS NULL THEN 1 else user_id end uid1
,partner_id
from odoo9.calendar_contacts   ON CONFLICT(id) DO NOTHING;
GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(calendar_contacts) odoo11 server from odoo9',cnt;	

ALTER TABLE public.calendar_contacts ENABLE TRIGGER ALL;



ALTER TABLE public.bus_presence DISABLE TRIGGER ALL;

	insert into public.bus_presence(	id
,status
,last_presence
,user_id
,last_poll
 )

	select id
,status
,last_presence
,user_id
,last_poll
from odoo9.bus_presence   ON CONFLICT(id) DO UPDATE SET status=excluded.status;
GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(bus_presence) odoo11 server from odoo9',cnt;	

ALTER TABLE public.bus_presence ENABLE TRIGGER ALL;

ALTER TABLE public.res_groups_users_rel DISABLE TRIGGER ALL;

	insert into public.res_groups_users_rel(gid
	,uid
 )

	select gid
	,uid
from odoo9.res_groups_users_rel   ON CONFLICT(gid, uid) DO UPDATE SET gid=excluded.gid,uid=excluded.uid;
GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_groups_users_rel) odoo11 server from odoo9',cnt;	

ALTER TABLE public.res_groups_users_rel ENABLE TRIGGER ALL;

-------------------------------------------------------------------------
/*
ALTER TABLE public.bus_bus DISABLE TRIGGER ALL;

insert into public.bus_bus(id
						  ,create_date
						  ,channel
						  ,message
						  ,create_uid
						  ,write_uid
						  ,write_date)
		select id
				,create_date
				,channel
				,message
				,create_uid
				,write_uid
				,write_date
		from odoo9.bus_bus ON CONFLICT (id) DO UPDATE SET 
		create_date=excluded.create_date
		,channel=excluded.channel
		,message=excluded.message
		,create_uid=excluded.create_uid
		,write_uid=excluded.write_uid
		,write_date=excluded.write_date;
		GET DIAGNOSTICS cnt = ROW_COUNT;

		RAISE NOTICE '% Records inserted into(bus_bus) odoo11 server from odoo9',cnt;
ALTER TABLE public.bus_bus ENABLE TRIGGER ALL;		

	
ALTER TABLE public.rule_group_rel DISABLE TRIGGER ALL;		

insert into public.rule_group_rel (rule_group_id,group_id)
		select rule_group_id,group_id
		from odoo9.rule_group_rel on 
			CONFLICT(rule_group_id,group_id) DO update set 
			rule_group_id=excluded.rule_group_id,
			group_id=excluded.group_id;
		GET DIAGNOSTICS cnt = ROW_COUNT;

		RAISE NOTICE '% Records inserted into(rule_group_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.rule_group_rel ENABLE TRIGGER ALL;
*/

/*				
ALTER TABLE public.res_groups_implied_rel DISABLE TRIGGER ALL;		
insert into public.res_groups_implied_rel(gid,hid)
			select gid,hid
			from odoo9.res_groups_implied_rel on 
			CONFLICT(gid,hid)  DO UPDATE set 
			gid=excluded.gid,
			hid=excluded.hid;
	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_groups_implied_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.res_groups_implied_rel ENABLE TRIGGER ALL;
*/
/*
ALTER TABLE public.res_company_users_rel DISABLE TRIGGER ALL;
insert into public.res_company_users_rel(cid,user_id)
			select cid,user_id
			from odoo9.res_company_users_rel on 
			CONFLICT(cid,user_id)  DO UPDATE set 
			cid=excluded.cid,
			user_id=excluded.user_id;
	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_company_users_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.res_company_users_rel ENABLE TRIGGER ALL;			
			
	
ALTER TABLE public.project_tags_project_task_rel DISABLE TRIGGER ALL;	
insert into public.project_tags_project_task_rel(project_task_id,project_tags_id)
			select project_task_id,project_tags_id
			from odoo9.project_tags_project_task_rel on 
			CONFLICT(project_task_id,project_tags_id) DO UPDATE set 
			project_task_id=excluded.project_task_id,
			project_tags_id=excluded.project_tags_id;
	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(project_tags_project_task_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.project_tags_project_task_rel ENABLE TRIGGER ALL;				
			
ALTER TABLE public.message_attachment_rel DISABLE TRIGGER ALL;			
insert into public.message_attachment_rel(message_id,attachment_id)
			select message_id,attachment_id
			from odoo9.message_attachment_rel 
			on CONFLICT(message_id,attachment_id) DO UPDATE set 
			message_id=excluded.message_id,
			attachment_id=excluded.attachment_id;
	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(message_attachment_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.message_attachment_rel ENABLE TRIGGER ALL;				
	
			
			
			
ALTER TABLE public.mail_tracking_value DISABLE TRIGGER ALL;				
INSERT INTO public.mail_tracking_value(id, 
field, 
field_desc, 
field_type, 
old_value_integer, 
old_value_float, 
old_value_monetary, 
old_value_char, 
old_value_text, 
old_value_datetime, 
new_value_integer, 
new_value_float, 
new_value_monetary, 
new_value_char, 
new_value_text, 
new_value_datetime, 
mail_message_id, 
create_uid, 
create_date, 
write_uid, 
write_date)

select 
id, 
field, 
field_desc, 
field_type, 
old_value_integer, 
old_value_float, 
old_value_monetary, 
old_value_char, 
old_value_text, 
old_value_datetime, 
new_value_integer, 
new_value_float, 
new_value_monetary, 
new_value_char, 
new_value_text, 
new_value_datetime, 
mail_message_id, 
create_uid, 
create_date, 
write_uid, 
write_date
from odoo9.mail_tracking_value on CONFLICT(id) DO UPDATE set 
field=excluded.field, 
field_desc=excluded.field_desc, 
field_type=excluded.field_type, 
old_value_integer=excluded.old_value_integer, 
old_value_float=excluded.old_value_float, 
old_value_monetary=excluded.old_value_monetary, 
old_value_char=excluded.old_value_char, 
old_value_text=excluded.old_value_text, 
old_value_datetime=excluded.old_value_datetime, 
new_value_integer=excluded.new_value_integer, 
new_value_float=excluded.new_value_float, 
new_value_monetary=excluded.new_value_monetary, 
new_value_char=excluded.new_value_char, 
new_value_text=excluded.new_value_text, 
new_value_datetime=excluded.new_value_datetime, 
mail_message_id=excluded.mail_message_id, 
create_uid=excluded.create_uid, 
create_date=excluded.create_date, 
write_uid=excluded.write_uid, 
write_date=excluded.write_date;
	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(mail_tracking_value) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_tracking_value ENABLE TRIGGER ALL;				
	*/		
/*			
ALTER TABLE public.mail_message_res_partner_needaction_rel DISABLE TRIGGER ALL;
INSERT INTO public.mail_message_res_partner_needaction_rel(
mail_message_id, 
res_partner_id 
)
select mail_message_id, 
res_partner_id
from odoo9.mail_message_res_partner_needaction_rel on CONFLICT(id) DO UPDATE set 
mail_message_id=excluded.mail_message_id,
res_partner_id=excluded.res_partner_id;
GET DIAGNOSTICS cnt = ROW_COUNT;
RAISE NOTICE '% Records inserted into(mail_message_res_partner_needaction_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_message_res_partner_needaction_rel ENABLE TRIGGER ALL;
*/


/*

ALTER TABLE public.mail_mail_res_partner_rel DISABLE TRIGGER ALL;
INSERT INTO public.mail_mail_res_partner_rel(mail_mail_id, 
res_partner_id)
select mail_mail_id, 
res_partner_id
from odoo9.mail_mail_res_partner_rel on CONFLICT(mail_mail_id, 
res_partner_id) DO UPDATE SET mail_mail_id=excluded.mail_mail_id, 
res_partner_id=excluded.res_partner_id;
GET DIAGNOSTICS cnt = ROW_COUNT;
RAISE NOTICE '% Records inserted into(mail_mail_res_partner_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_mail_res_partner_rel ENABLE TRIGGER ALL;


ALTER TABLE public.mail_mail DISABLE TRIGGER ALL;
INSERT INTO public.mail_mail(id, 
mail_message_id, 
body_html, 
"references", 
headers, 
notification, 
email_to, 
email_cc, 
state, 
auto_delete, 
failure_reason, 
create_uid, 
create_date, 
write_uid, 
write_date, 
fetchmail_server_id)
select id, 
mail_message_id, 
body_html, 
"references", 
headers, 
notification, 
email_to, 
email_cc, 
state, 
auto_delete, 
failure_reason, 
create_uid, 
create_date, 
write_uid, 
write_date, 
fetchmail_server_id
from odoo9.mail_mail ON CONFLICT(id) DO UPDATE SET 
mail_message_id=excluded.mail_message_id, 
body_html =excluded.body_html, 
"references"=excluded.references, 
headers=excluded.headers, 
notification =excluded.notification, 
email_to=excluded.email_to, 
email_cc =excluded.email_cc, 
state =excluded.state, 
auto_delete =excluded.auto_delete, 
failure_reason=excluded.failure_reason, 
create_uid =excluded.create_uid, 
create_date =excluded.create_date, 
write_uid =excluded.write_uid, 
write_date=excluded.write_date;
GET DIAGNOSTICS cnt = ROW_COUNT;
RAISE NOTICE '% Records inserted into(mail_mail) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_mail ENABLE TRIGGER ALL;




ALTER TABLE public.mail_followers_mail_message_subtype_rel DISABLE TRIGGER ALL;
INSERT INTO public.mail_followers_mail_message_subtype_rel( mail_followers_id, 
mail_message_subtype_id)
select mail_followers_id, 
mail_message_subtype_id
from odoo9.mail_followers_mail_message_subtype_rel ON CONFLICT(mail_followers_id,mail_message_subtype_id) DO UPDATE SET 
mail_followers_id=excluded.mail_followers_id,
mail_message_subtype_id=excluded.mail_message_subtype_id;
GET DIAGNOSTICS cnt = ROW_COUNT;
RAISE NOTICE '% Records inserted into(mail_followers_mail_message_subtype_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_followers_mail_message_subtype_rel ENABLE TRIGGER ALL;



ALTER TABLE public.mail_followers DISABLE TRIGGER ALL;
INSERT INTO public.mail_followers( id, 
res_model, 
res_id, 
partner_id, 
channel_id)
select id, 
res_model, 
res_id, 
partner_id, 
channel_id
from odoo9.mail_followers on CONFLICT(id) DO UPDATE SET 
res_model=excluded.res_model, 
res_id=excluded.res_id, 
partner_id=excluded.partner_id, 
channel_id=excluded.channel_id;
GET DIAGNOSTICS cnt = ROW_COUNT;
RAISE NOTICE '% Records inserted into(mail_followers) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_followers ENABLE TRIGGER ALL;
*/
-------------------------------------------------------------------------




end_time:=CLOCK_TIMESTAMP();

age_value:=end_time-start_time;

	RETURN age_value;

	

	exception 

    when others then

        RAISE INFO 'Error Name:%',SQLERRM;

        RAISE INFO 'Error State:%', SQLSTATE;

        return age_value;

END



$BODY$

  LANGUAGE plpgsql VOLATILE

  COST 100;
------------------------------------------------------
-- FUNCTION: public.leaves_module_function()

-- DROP FUNCTION public.leaves_module_function();

CREATE OR REPLACE FUNCTION public.leaves_module_function(
	)
    RETURNS interval
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
AS $BODY$

 DECLARE cnt INT DEFAULT 0;
 DECLARE age_value interval ;
 DECLARE start_time TIME ;
 DECLARE end_time TIME ;
BEGIN
start_time:=CLOCK_TIMESTAMP();
ALTER TABLE public.hr_holidays DISABLE TRIGGER ALL;

	INSERT INTO public.hr_holidays (id
				,name 
				,state 
				,payslip_status 
				,report_note 
				,user_id 
				,date_from 
				,date_to 
				,holiday_status_id 
				,employee_id 
				,manager_id 
				,notes 
				,number_of_days_temp 
				,number_of_days
				,meeting_id 
				,type
				,parent_id 
				,department_id 
				,category_id 
				,holiday_type
				,message_last_post 
				,create_uid 
				,create_date 
				,write_uid 
				,write_date)
				
		SELECT id
				,name 
				,state 
				,payslip_status 
				,report_note 
				,user_id 
				,date_from 
				,date_to 
				,holiday_status_id 
				,employee_id 
				,manager_id 
				,notes 
				,number_of_days_temp 
				,number_of_days
				,meeting_id 
				,type
				,parent_id 
				,department_id 
				,category_id 
				,holiday_type
				,message_last_post 
				,create_uid 
				,create_date 
				,write_uid 
				,write_date
	FROM odoo9.hr_holidays ;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(hr_holidays) odoo11 server from odoo9',cnt;
ALTER TABLE public.hr_holidays ENABLE TRIGGER ALL;

ALTER TABLE public.hr_compoff DISABLE TRIGGER ALL;
	INSERT INTO public.hr_compoff (name 
				,state 
				,payslip_status 
				,report_note 
				,date_from 
				,date_to 
				,holiday_status_id 
				,employee_id 
				,notes 
				,number_of_days_temp 
				,meeting_id 
				,type
				,department_id 
				,category_id 
				,holiday_type
				,message_last_post 
				,create_uid 
				,create_date 
				,write_uid 
				,write_date)
				
		SELECT name 
				,state 
				,payslip_status 
				,report_note 
				,case when date_from IS NOT NULL then date_from else '2000-01-01 01:01:01' end as  date_from
				,case when date_to IS NOT NULL then date_to else '2000-01-01 01:01:01' end as  date_to
				,holiday_status_id::text 
				,employee_id  
				,notes 
				,number_of_days_temp 
				,meeting_id 
				,type
				,department_id 
				,category_id 
				,holiday_type
				,message_last_post 
				,create_uid 
				,create_date 
				,write_uid 
				,write_date
	FROM public.hr_holidays where holiday_status_id=6 and type='add';
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(hr_compoff) odoo11 server from odoo9',cnt;
ALTER TABLE public.hr_compoff ENABLE TRIGGER ALL; 	

ALTER TABLE public.hr_holidays_status DISABLE TRIGGER ALL;

	INSERT INTO public.hr_holidays_status( id,
				name, 
				categ_id ,
				color_name,
				"limit" ,
				active ,
				double_validation ,
				company_id ,
				create_uid ,
				create_date,
				write_uid ,
				write_date)
		select id,
				name, 
				categ_id ,
				color_name,
				"limit" ,
				active ,
				double_validation ,
				company_id ,
				create_uid ,
				create_date,
				write_uid ,
				write_date
	from odoo9.hr_holidays_status;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(hr_holidays_status) odoo11 server from odoo9',cnt;

ALTER TABLE public.hr_holidays_status ENABLE TRIGGER ALL;	

	
ALTER TABLE public.hr_holidays_summary_dept DISABLE TRIGGER ALL;

	INSERT INTO public.hr_holidays_summary_dept (id 
				,date_from 
				,holiday_type 
				,create_uid 
				,create_date 
				,write_uid 
				,write_date)
		SELECT  id 
				,date_from 
				,holiday_type 
				,create_uid 
				,create_date 
				,write_uid 
				,write_date 
	FROM odoo9.hr_holidays_summary_dept;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(hr_holidays_summary_dept) odoo11 server from odoo9',cnt;
	
ALTER TABLE public.hr_holidays_summary_dept ENABLE TRIGGER ALL; 

ALTER TABLE public.hr_holidays_summary_employee DISABLE TRIGGER ALL;

	insert into public.hr_holidays_summary_employee(
					id,
					create_uid,
					create_date,
					date_from,
					holiday_type,
					write_date,
					write_uid)
			select id,
					create_uid,
					create_date,
					date_from,
					holiday_type,
					write_date,
					write_uid
	from  odoo9.hr_holidays_summary_employee;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(hr_holidays_summary_employee) odoo11 server from odoo9',cnt;

ALTER TABLE public.hr_holidays_summary_employee ENABLE TRIGGER ALL; 
		
			
ALTER TABLE public.resource_calendar_leaves DISABLE TRIGGER ALL;

	insert into public.resource_calendar_leaves(
				id,
				create_uid,
				create_date,
				name,
				resource_id,
				date_from,
				company_id,
				write_uid,
				write_date,
				date_to,
				calendar_id,
				holiday_id)
				
		select id,
				create_uid,
				create_date,
				name,
				resource_id,
				date_from,
				company_id,
				write_uid,
				write_date,
				date_to,
				calendar_id,
				holiday_id
	from  odoo9.resource_calendar_leaves;

	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(resource_calendar_leaves) odoo11 server from odoo9',cnt;
ALTER TABLE public.resource_calendar_leaves ENABLE TRIGGER ALL; 
 
end_time:=CLOCK_TIMESTAMP();
age_value:=end_time-start_time;
	RETURN age_value;
	
	exception 
    when others then
        RAISE INFO 'Error Name:%',SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
        return age_value;
END

$BODY$;

ALTER FUNCTION public.leaves_module_function()
    OWNER TO openpg;
	
	
------------------------------------------------------------------ 
  
-- FUNCTION: public.sprint_module_function()

-- DROP FUNCTION public.sprint_module_function();

CREATE OR REPLACE FUNCTION public.sprint_module_function(
	)
    RETURNS interval
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
AS $BODY$

 DECLARE cnt INT DEFAULT 0;
 DECLARE age_value interval ;
 DECLARE start_time TIME ;
 DECLARE end_time TIME ;
BEGIN
start_time:=CLOCK_TIMESTAMP();
/*
ALTER TABLE public.res_users DISABLE TRIGGER ALL;

	INSERT INTO public.res_users (  id,
			active,
			login ,
			password ,
			company_id ,
			partner_id ,
			signature ,
			action_id ,
			share ,
			create_uid ,
			create_date,
			write_uid ,
			write_date ,
			password_crypt ,
			alias_id ,
			notification_type )
										
		SELECT  id,
			active,
			login ,
			password ,
			company_id ,
			partner_id ,
			signature ,
			action_id ,
			share ,
			create_uid ,
			create_date,
			write_uid ,
			write_date ,
			password_crypt, 
			alias_id ,
			'email' notification_type  
	FROM odoo9.res_users where id>10;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(res_users) odoo11 server from odoo9',cnt;
	
ALTER TABLE public.res_users ENABLE TRIGGER ALL; 

ALTER TABLE public.res_company DISABLE TRIGGER ALL;
	insert into public.res_company(
				name ,
				partner_id ,
				currency_id,
				parent_id ,
				logo_web ,
				account_no ,
				email ,
				phone ,
				company_registry ,
				paperformat_id ,
				create_uid ,
				create_date,
				write_uid ,
				write_date ,
				project_time_mode_id ,
				fiscalyear_last_day ,
				fiscalyear_last_month ,
				period_lock_date ,
				fiscalyear_lock_date ,
				transfer_account_id ,
				expects_chart_of_accounts ,
				chart_template_id ,
				bank_account_code_prefix ,
				cash_account_code_prefix ,
				accounts_code_digits ,
				tax_calculation_rounding_method ,
				currency_exchange_journal_id ,
				anglo_saxon_accounting ,
				property_stock_account_input_categ_id ,
				property_stock_account_output_categ_id ,
				property_stock_valuation_account_id ,
				overdue_msg )
				
		select name ,
				partner_id ,
				currency_id,
				parent_id ,
				logo_web ,
				account_no ,
				email ,
				phone ,
				company_registry ,
				paperformat_id ,
				create_uid ,
				create_date,
				write_uid ,
				write_date ,
				project_time_mode_id ,
				fiscalyear_last_day ,
				fiscalyear_last_month ,
				period_lock_date ,
				fiscalyear_lock_date ,
				transfer_account_id ,
				expects_chart_of_accounts ,
				chart_template_id ,
				bank_account_code_prefix ,
				cash_account_code_prefix ,
				accounts_code_digits ,
				tax_calculation_rounding_method ,
				currency_exchange_journal_id ,
				anglo_saxon_accounting ,
				property_stock_account_input_categ_id ,
				property_stock_account_output_categ_id ,
				property_stock_valuation_account_id ,
				overdue_msg 
	from odoo9.res_company;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(res_company) odoo11 server from odoo9',cnt;
	
ALTER TABLE public.res_company ENABLE TRIGGER ALL;	

ALTER TABLE public.res_partner DISABLE TRIGGER ALL;

	INSERT INTO public.res_partner (id,
			name ,
			company_id ,
			display_name ,
			date ,
			title,
			parent_id ,
			ref ,
			lang ,
			invoice_warn,
			tz ,
			user_id ,
			vat ,
			website ,
			comment ,
			credit_limit ,
			barcode ,
			active ,
			customer ,
			supplier ,
			employee ,
			function ,
			type ,
			street ,
			street2 ,
			zip ,
			city ,
			state_id ,
			country_id ,
			email ,
			phone ,
			mobile,
			is_company ,
			color ,
			commercial_partner_id ,
			create_date ,
			write_uid ,
			write_date,
			message_last_post ,
			opt_out ,
			signup_token ,
			signup_type ,
			signup_expiration ,
			calendar_last_notif_ack ,
			debit_limit ,
			last_time_entries_checked )
			
		select id,
			name ,
			company_id ,
			display_name ,
			date ,
			title,
			parent_id ,
			ref ,
			lang ,
			'AA' invoice_warn,
			tz ,
			user_id ,
			vat ,
			website ,
			comment ,
			credit_limit ,
			barcode ,
			active ,
			customer ,
			supplier ,
			employee ,
			function ,
			type ,
			street ,
			street2 ,
			zip ,
			city ,
			state_id ,
			country_id ,
			email ,
			phone ,
			mobile,
			is_company ,
			color ,
			commercial_partner_id ,
			create_date ,
			write_uid ,
			write_date,
			message_last_post ,
			opt_out ,
			signup_token ,
			signup_type ,
			signup_expiration ,
			calendar_last_notif_ack ,
			debit_limit ,
			last_time_entries_checked 
	from odoo9.res_partner where id>10;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(res_partner) odoo11 server from odoo9',cnt;

ALTER TABLE public.res_partner ENABLE TRIGGER ALL;	
*/

ALTER TABLE public.resource_calendar DISABLE TRIGGER ALL;
INSERT INTO public.resource_calendar(id,
									 name,
									 company_id,
									 create_uid,
									 create_date,
									 write_uid,
									 write_date)
							  select id,
									 name,
									 company_id,
									 create_uid,
									 create_date,
									 write_uid,
									 write_date 
							  from odoo9.resource_calendar;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(resource_calendar) odoo11 server from odoo9',cnt;
ALTER TABLE public.resource_calendar ENABLE TRIGGER ALL;	



ALTER TABLE public.ir_attachment DISABLE TRIGGER ALL;
INSERT INTO public.ir_attachment(id,
								 create_date,
								 write_date,
								 res_model,
								 write_uid,
								 res_name,
								 db_datas,
								 file_size,
								 create_uid,
								 company_id,
								 index_content,
								 type,
								 public,
								 store_fname,
								 description,
								 res_field,
								 mimetype,
								 name,
								 url,
								 res_id,
								 checksum,
								 datas_fname)
						select 	 id,
								 create_date,
								 write_date,
								 CASE WHEN res_model='project.issue' THEN 'project.task' else res_model end res_mo,
								 write_uid,
								 res_name,
								 db_datas,
								 file_size,
								 create_uid,
								 company_id,
								 index_content,
								 type,
								 public,
								 store_fname,
								 description,
								 res_field,
								 mimetype,
								 name,
								 url,
								 res_id,
								 checksum,
								 datas_fname
						from odoo9.ir_attachment where id>328 ON CONFLICT(id) DO NOTHING; 
						/*set create_date=excluded.create_date,
							write_date=excluded.write_date,
							res_model=excluded.res_model,
							write_uid=excluded.write_uid,
							res_name=excluded.res_name,
							db_datas=excluded.db_datas,
							file_size=excluded.file_size,
							create_uid=excluded.create_uid,
							company_id=excluded.company_id,
							index_content=excluded.index_content,
							type=excluded.type,
							public=excluded.public,
							store_fname=excluded.store_fname,
							description=excluded.description,
							res_field=excluded.res_field,
							mimetype=excluded.mimetype,
							name=excluded.name,
							url=excluded.url,
							res_id=excluded.res_id,
							checksum=excluded.checksum,
							datas_fname=excluded.datas_fname;--where id>335;*/
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(ir_attachment) odoo11 server from odoo9',cnt;
				
ALTER TABLE public.ir_attachment ENABLE TRIGGER ALL;	
	
	
ALTER TABLE public.project_task DISABLE TRIGGER ALL;

	insert into public.project_task(id
			,name
			,description
			,priority
			,active
			,stage_id 
			,kanban_state
			,create_date
			,write_date
			,date_deadline 
			,date_last_stage_update
			,project_id
			,user_id 
			,partner_id
			,company_id
			,color 
			,email_from
			,email_cc
			,working_hours_open 
			,working_hours_close
			,message_last_post
			,create_uid
			,write_uid
			,progress
			,severity
			,issue_type
			,issue_status
			,task_type
			,fixed_in_sprint
			,no_of_tests_impacted
			,fixed_in_build
			,sprint_id
			,rasised_by)

		select id
			,name
			,description
			,x_priority
			,'t'
			,stage_id 
			,kanban_state
			,create_date
			,write_date
			,date_deadline 
			,date_last_stage_update
			,project_id
			,user_id 
			,partner_id
			,company_id
			,color 
			,email_from
			,email_cc
			,working_hours_open 
			,working_hours_close
			,message_last_post
			,create_uid
			,write_uid
			,progress
			,x_severity
			,x_issue_type
			,x_issue_status
			,'issue'
			,CASE WHEN x_fixed_in_sprint>0 THEN x_fixed_in_sprint ELSE NULL END fixed_sprint
			,x_no_of_tests_impacted
			,x_fixed_in_build
			,x_sprint_id
			,x_raised_by
	from odoo9.project_issue  ON CONFLICT(id) DO UPDATE
	SET name=excluded.name
		,description=excluded.description
		,priority=excluded.priority
		,active='t'
		,stage_id =excluded.stage_id 
		,kanban_state=excluded.kanban_state
		,create_date=excluded.create_date
		,write_date=excluded.write_date
		,date_deadline =excluded.date_deadline 
		,date_last_stage_update=excluded.date_last_stage_update
		,project_id=excluded.project_id
		,user_id =excluded.user_id 
		,partner_id=excluded.partner_id
		,company_id=excluded.company_id
		,color =excluded.color 
		,email_from=excluded.email_from
		,email_cc=excluded.email_cc
		,working_hours_open =excluded.working_hours_open 
		,working_hours_close=excluded.working_hours_close
		,message_last_post=excluded.message_last_post
		,create_uid=excluded.create_uid
		,write_uid=excluded.write_uid
		,progress=excluded.progress
		,severity=excluded.severity
		,issue_type=excluded.issue_type
		,issue_status=excluded.issue_status
		,task_type='issue'
		,fixed_in_sprint=excluded.fixed_in_sprint
		,no_of_tests_impacted=excluded.no_of_tests_impacted
		,fixed_in_build=excluded.fixed_in_build
		,sprint_id=excluded.sprint_id;--where project_id!=3;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(project_task) odoo11 server from odoo9',cnt;
ALTER TABLE public.project_task ENABLE TRIGGER ALL; 

	
ALTER TABLE public.project_task_type DISABLE TRIGGER ALL;

INSERT INTO public.project_task_type(id
									,name
									,description
									,sequence
									,legend_priority
									,legend_blocked
									,legend_done
									,legend_normal
									,fold
									,create_uid
									,create_date
									,write_uid
									,write_date)
						select      id
									,name
									,description
									,sequence
									,legend_priority
									,'Blocked'
									,'Ready for Next Stage'
									,'In Progress'
									,fold
									,create_uid
									,create_date
									,write_uid
									,write_date
							from odoo9.project_task_type ON CONFLICT(id) DO NOTHING ;--where id>3;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(project_task_type) odoo11 server from odoo9',cnt;							
ALTER TABLE public.project_task_type ENABLE TRIGGER ALL;		

ALTER TABLE public.project_task DISABLE TRIGGER ALL;

	INSERT INTO public.project_task (id
	                                 ,create_date
									 ,sequence
	                                 ,color
	                                 ,end_date
	                                 ,write_uid
	                                 ,planned_hours
	                                 ,partner_id
	                                 ,create_uid
	                                 ,displayed_image_id
	                                 ,user_id
	                                 ,start_date
	                                 ,message_last_post
	                                 ,company_id
	                                 ,project_id
	                                 ,date_last_stage_update
	                                 ,date_assign
	                                 ,description
	                                 ,kanban_state
	                                 ,write_date
	                                 ,active
	                                 ,stage_id
	                                 ,name
	                                 ,date_deadline
	                                 ,notes 
	                                 ,remaining_hours
	                                 ,effective_hours
	                                 --,analytic_account_id
	                                 ,progress
	                                 ,delay_hours
	                                 ,total_hours
	                                 --,procurement_id
	                                 --,sale_line_id
	                                 ,sprint_id
	                                 ,billable
	                                 ,requirement_name
	                                 ,dev_type
	                                 ,technical
	                                 ,estimated_hours
	                                 ,actual_hours
	                                 ,status
	                                 ,requirement_id
	                                 ,priority
									 ,task_type
									 ,date_start
									 ,date_end
									 )
		SELECT id
               ,create_date

               ,sequence
               ,color
               ,date_end
               ,write_uid
               ,planned_hours
               ,partner_id
               ,create_uid
               ,displayed_image_id
               ,user_id
               ,date_start
               ,message_last_post
               ,company_id
               ,project_id
               ,date_last_stage_update
               ,date_assign
		       ,description
		       ,kanban_state
		       ,write_date
		       ,'TRUE'
		       ,stage_id
		       ,name
		       ,date_deadline
		       ,notes 
		       ,remaining_hours
		       ,effective_hours
               --,analytic_account_id
               ,progress
               ,delay_hours
               ,total_hours
               --,procurement_id
               --,sale_line_id
               ,sprint_id
               ,x_bill
               ,x_requirement_name
               ,x_dev_type
               ,x_tech
               ,x_estimated_hours
               ,x_actual_hours
               ,x_status
               ,x_requirement_id
               ,x_priority
			   ,'task'
			   ,date_start
			   ,date_end
	FROM odoo9.project_task ON CONFLICT(id) DO UPDATE
	SET 
		create_date=excluded.create_date
		,sequence=excluded.sequence
		,color=excluded.color
		,end_date=excluded.end_date
		,write_uid=excluded.write_uid
		,planned_hours=excluded.planned_hours
		,partner_id=excluded.partner_id
		,create_uid=excluded.create_uid
		,displayed_image_id=excluded.displayed_image_id
		,user_id=excluded.user_id
		,start_date=excluded.start_date
		,message_last_post=excluded.message_last_post
		,company_id=excluded.company_id
		,project_id=excluded.project_id
		,date_last_stage_update=excluded.date_last_stage_update
		,date_assign=excluded.date_assign
		,description=excluded.description
		,kanban_state=excluded.kanban_state
		,write_date=excluded.write_date
		,active='t'
		,stage_id=excluded.stage_id
		,name=excluded.name
		,date_deadline=excluded.date_deadline
		,notes =excluded.notes 
		,remaining_hours=excluded.remaining_hours
		,effective_hours=excluded.effective_hours
		,progress=excluded.progress
		,delay_hours=excluded.delay_hours
		,total_hours=excluded.total_hours
		,sprint_id=excluded.sprint_id
		,billable=excluded.billable
		,requirement_name=excluded.requirement_name
		,dev_type=excluded.dev_type
		,technical=excluded.technical
		,estimated_hours=excluded.estimated_hours
		,actual_hours=excluded.actual_hours
		,status=excluded.status
		,requirement_id=excluded.requirement_id
		,priority=excluded.priority
		,task_type='task'
		,date_start=excluded.date_start
		,date_end=excluded.date_end	;--where project_id!=3;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(project_task) odoo11 server from odoo9',cnt;
	
ALTER TABLE public.project_task ENABLE TRIGGER ALL; 

ALTER TABLE public.project_sprint DISABLE TRIGGER ALL;

	INSERT INTO public.project_sprint (id ,
				                    is_current_sprint,
				                    create_uid,
				                    display_name,
				                    name,
				                    end_date,
				                    start_date,
				                    write_uid,
				                    is_previous_sprint,
				                    write_date,
				                    scrum_team_id,
				                    create_date)
						SELECT id ,
						       is_current_sprint,
						       create_uid,
						       display_name,
						       name,
						       end_date,
						       start_date,
						       write_uid,
						       is_previous_sprint,
						       write_date,
						       scrum_team_id,
						       create_date
	FROM odoo9.project_sprint;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(project_sprint) odoo11 server from odoo9',cnt;
ALTER TABLE public.project_sprint ENABLE TRIGGER ALL;

ALTER TABLE public.project_scrum_team DISABLE TRIGGER ALL;
	INSERT INTO public.project_scrum_team (id 
										   ,create_uid
										   ,create_date
										   ,name
										   ,write_uid
										   ,write_date)
		SELECT  id 
			   ,create_uid
			   ,create_date
			   ,name
			   ,write_uid
			   ,write_date
	FROM odoo9.project_scrum_team;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(project_scrum_team) odoo11 server from odoo9',cnt;
ALTER TABLE public.project_scrum_team ENABLE TRIGGER ALL; 	

/*ALTER TABLE public.mail_alias DISABLE TRIGGER ALL;

	insert into public.mail_alias( id 
								  ,alias_name 
								  ,alias_model_id
								  ,alias_user_id
								  ,alias_defaults
								  ,alias_force_thread_id
								  ,alias_parent_model_id
								  ,alias_parent_thread_id
								  ,alias_contact
								  ,create_uid
								  ,create_date
								  ,write_uid
								  ,write_date)
			select  id 
					,alias_name 
					,alias_model_id
					,alias_user_id
					,alias_defaults
					,alias_force_thread_id
					,alias_parent_model_id
					,alias_parent_thread_id
					,alias_contact
					,create_uid
					,create_date
					,write_uid
					,write_date 
			
	from  odoo9.mail_alias ON CONFLICT(id) DO NOTHING ;--where id>3;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(mail_alias) odoo11 server from odoo9',cnt;
	ALTER TABLE public.mail_alias ENABLE TRIGGER ALL; 
	
	*/
	
/*ALTER TABLE public.mail_template DISABLE TRIGGER ALL;

	insert into public.mail_template(id 
	                                 ,create_date
	                                 ,write_date
	                                 ,auto_delete 
	                                 ,mail_server_id
	                                 ,write_uid
	                                 ,partner_to 
	                                 ,ref_ir_act_window 
	                                 ,subject
	                                 ,create_uid 
	                                 ,report_template
	                                 ,user_signature
	                                 ,null_value
	                                 ,email_cc 
	                                 ,model_id 
	                                 ,sub_model_object_field
	                                 ,body_html
	                                 ,email_to
	                                 ,sub_object
	                                 ,copyvalue
	                                 ,lang
	                                 ,name
	                                 ,model_object_field
	                                 ,report_name
	                                 ,use_default_to
	                                 ,reply_to
	                                 ,model
	                                 ,email_from)
	select id 
	       ,create_date
	       ,write_date
	       ,auto_delete 
	       ,mail_server_id
	       ,write_uid
	       ,partner_to 
	       ,ref_ir_act_window 
	       ,subject
	       ,create_uid 
	       ,report_template
	       ,user_signature
	       ,null_value
	       ,email_cc 
	       ,model_id 
	       ,sub_model_object_field
	       ,body_html
	       ,email_to
	       ,sub_object
	       ,copyvalue
	       ,lang
	       ,name
	       ,model_object_field
	       ,report_name
	       ,use_default_to
	       ,reply_to
	       ,model
	       ,email_from
	from  odoo9.mail_template ON CONFLICT(id) DO UPDATE
		SET create_date=excluded.create_date
			,write_date=excluded.write_date
			,auto_delete =excluded.auto_delete 
			,mail_server_id=excluded.mail_server_id
			,write_uid=excluded.write_uid
			,partner_to =excluded.partner_to 
			,ref_ir_act_window =excluded.ref_ir_act_window 
			,subject=excluded.subject
			,create_uid =excluded.create_uid 
			,report_template=excluded.report_template
			,user_signature=excluded.user_signature
			,null_value=excluded.null_value
			,email_cc =excluded.email_cc 
			,model_id =excluded.model_id 
			,sub_model_object_field=excluded.sub_model_object_field
			,body_html=excluded.body_html
			,email_to=excluded.email_to
			,sub_object=excluded.sub_object
			,copyvalue=excluded.copyvalue
			,lang=excluded.lang
			,name=excluded.name
			,model_object_field=excluded.model_object_field
			,report_name=excluded.report_name
			,use_default_to=excluded.use_default_to
			,reply_to=excluded.reply_to
			,model=excluded.model
			,email_from=excluded.email_from;--where id>14;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(mail_template) odoo11 server from odoo9',cnt;
	ALTER TABLE public.mail_template ENABLE TRIGGER ALL; 		
*/
	
ALTER TABLE public.project_tags DISABLE TRIGGER ALL;
insert into public.project_tags (id
								,name
								,color
								,create_uid
								,create_date
								,write_uid
								,write_date)
						select id
								,name
								,color
								,create_uid
								,create_date
								,write_uid
								,write_date
						from odoo9.project_tags  ON CONFLICT(id) DO NOTHING;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(project_tags) odoo11 server from odoo9',cnt; 
ALTER TABLE public.project_tags ENABLE TRIGGER ALL;		
	
	
ALTER TABLE public.project_project DISABLE TRIGGER ALL;

	INSERT INTO public.project_project(id 
	                                   ,active
	                                   ,create_date
	                                   ,color
	                                   ,alias_id
	                                   ,write_uid
	                                   ,privacy_visibility
	                                   ,label_tasks
	                                   ,analytic_account_id
	                                   ,create_uid
	                                   ,user_id
	                                   ,date_start
	                                   ,message_last_post
	                                   ,state			--not null
	                                   ,sequence
	                                   ,write_date
	                                   ,date
	                                   ,resource_calendar_id
	                                   --,label_issues
	                                   ,scrum_team_id
									   ,subtask_project_id
									   ,allow_timesheets
									   --,alias_model
									   )	

		select id 
		       ,'TRUE'
		       ,create_date
		       ,color
		       ,alias_id
		       ,write_uid
		       ,privacy_visibility
		       ,label_tasks
		       ,analytic_account_id
		       ,create_uid
		       ,user_id
		       ,date_start
		       ,message_last_post
		       ,state
		       ,sequence
		       ,write_date
		       ,date
		       ,CASE WHEN resource_calendar_id IS NULL THEN 1 else resource_calendar_id end 
		       --,label_issues
		       ,scrum_team_id
			   ,id
			   ,'t'
			   --,alias_model
	from odoo9.project_project ON CONFLICT(id) DO UPDATE 
		SET active='t'
	        ,create_date=excluded.create_date
	        ,color=excluded.color
	        ,alias_id=excluded.alias_id
	        ,write_uid=excluded.write_uid
	        ,privacy_visibility=excluded.privacy_visibility
	        ,label_tasks=excluded.label_tasks
	        ,analytic_account_id=excluded.analytic_account_id
	        ,create_uid=excluded.create_uid
	        ,user_id=excluded.user_id
	        ,date_start=excluded.date_start
	        ,message_last_post=excluded.message_last_post
	        ,state=excluded.state			--not null
	        ,sequence=excluded.sequence
	        ,write_date=excluded.write_date
	        ,date=excluded.date
	        ,resource_calendar_id=excluded.resource_calendar_id
	        ,scrum_team_id=excluded.scrum_team_id
			,subtask_project_id=excluded.id
			,allow_timesheets='t';
			--,alias_model=excluded.alias_model;--where id!=3 --where id>3;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(project_project) odoo11 server from odoo9',cnt;

	
	update public.project_project set active='t';
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records updated in project_project table in odoo11 server ',cnt;

ALTER TABLE public.project_project ENABLE TRIGGER ALL;	

ALTER TABLE public.mail_message DISABLE TRIGGER ALL;

	insert into public.mail_message(id
								,create_date
								,write_date
								,mail_server_id
								,write_uid
								,subject
								,create_uid
								,parent_id
								,subtype_id
								,res_id
								,message_id
								,body
								,record_name
								,no_auto_thread
								,date
								,model
								,reply_to
								,author_id
								,message_type
								,email_from)

						select id
								,create_date
								,write_date
								,mail_server_id
								,write_uid
								,subject
								,create_uid
								,parent_id
								,subtype_id
								,res_id
								,message_id
								,body
								,record_name
								,no_auto_thread
								,date
								,CASE WHEN model='project.issue' THEN 'project.task' else model end model1
								,reply_to
								,author_id
								,message_type
								,email_from
	from odoo9.mail_message  ON CONFLICT(id) DO UPDATE
	SET id=excluded.id
		,create_date=excluded.create_date
		,write_date=excluded.write_date
		,mail_server_id=excluded.mail_server_id
		,write_uid=excluded.write_uid
		,subject=excluded.subject
		,create_uid=excluded.create_uid
		,parent_id=excluded.parent_id
		,subtype_id=excluded.subtype_id
		,res_id=excluded.res_id
		,message_id=excluded.message_id
		,body=excluded.body
		,record_name=excluded.record_name
		,no_auto_thread=excluded.no_auto_thread
		,date=excluded.date
		,model=excluded.model
		,reply_to=excluded.reply_to
		,author_id=excluded.author_id
		,message_type=excluded.message_type
		,email_from=excluded.email_from;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(mail_message) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_message ENABLE TRIGGER ALL; 


ALTER TABLE public.mail_message_subtype DISABLE TRIGGER ALL;

	insert into public.mail_message_subtype(id
,create_uid
,create_date
,description
,sequence
,"default"
,res_model
,write_uid
,parent_id
,internal
,write_date
,relation_field
,hidden
,name)

						select id
,create_uid
,create_date
,description
,sequence
,"default"
,res_model
,write_uid
,parent_id
,internal
,write_date
,relation_field
,hidden
,name
	from odoo9.mail_message_subtype  ON CONFLICT(id) DO NOTHING;
	GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(mail_message_subtype) odoo11 server from odoo9',cnt;
ALTER TABLE public.mail_message_subtype ENABLE TRIGGER ALL; 


ALTER TABLE public.res_company_users_rel DISABLE TRIGGER ALL; 
insert into public.res_company_users_rel 
select *from odoo9.res_company_users_rel
 ON CONFLICT(cid,user_id) DO update set user_id=excluded.user_id;
 GET DIAGNOSTICS cnt = ROW_COUNT;
	RAISE NOTICE '% Records inserted into(res_company_users_rel) odoo11 server from odoo9',cnt;
ALTER TABLE public.res_company_users_rel ENABLE TRIGGER ALL; 


end_time:=CLOCK_TIMESTAMP();
age_value:=end_time-start_time;
	RETURN age_value;
	
	exception 
    when others then
        RAISE INFO 'Error Name:%',SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
        return age_value;
END

$BODY$;

-------------------------------------------------------
-- FUNCTION: public.website_module_function()



-- DROP FUNCTION public.website_module_function();



CREATE OR REPLACE FUNCTION public.website_module_function(

	)

    RETURNS interval

    LANGUAGE 'plpgsql'

    COST 100

    VOLATILE 

AS $BODY$



 DECLARE cnt INT DEFAULT 0;

 DECLARE age_value interval ;

 DECLARE start_time TIME ;

 DECLARE end_time TIME ;

BEGIN

start_time:=CLOCK_TIMESTAMP();



ALTER TABLE public.website_support_ticket DISABLE TRIGGER ALL;

INSERT INTO public.website_support_ticket(id

							             ,create_date

							             ,priority_id

							             ,write_uid

							             ,partner_id

							             ,subject

							             ,category

							             ,create_uid

							             ,portal_access_key

							             ,message_last_post

							             ,company_id

							             ,state

							             ,attachment

							             ,unattended

							             ,email

							             ,person_name

							             ,description

							             ,attachment_filename

							             ,write_date

							             ,ticket_number

							  )

							  select  id

							          ,create_date

							          ,priority_id

							          ,write_uid

							          ,partner_id

							          ,subject

							          ,category

							          ,create_uid

							          ,portal_access_key

							          ,message_last_post

							          ,company_id

							          ,state

							          ,attachment

							          ,unattended

							          ,email

							          ,person_name

							          ,description

							          ,attachment_filename

							          ,write_date

							          ,ticket_number

				 from odoo9.website_support_ticket;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(website_support_ticket) odoo11 server from odoo9',cnt;

ALTER TABLE public.website_support_ticket ENABLE TRIGGER ALL;



ALTER TABLE public.website_support_ticket_categories DISABLE TRIGGER ALL;

INSERT INTO public.website_support_ticket_categories(id

													,create_uid

													,create_date

													,name

													,write_uid

													,write_date)

											select  id

													,create_uid

													,create_date

													,name

													,write_uid

													,write_date

				 from odoo9.website_support_ticket_categories ON CONFLICT(id) DO update set id=excluded.id,create_uid=excluded.create_uid,write_uid=excluded.write_uid,name=excluded.name,create_date=excluded.create_date,write_date=excluded.write_date;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(website_support_ticket_categories) odoo11 server from odoo9',cnt;

ALTER TABLE public.website_support_ticket_categories ENABLE TRIGGER ALL;





ALTER TABLE public.website_support_ticket_priority DISABLE TRIGGER ALL;

INSERT INTO public.website_support_ticket_priority(id 

												  ,create_uid

												  ,create_date

												  ,name

												  ,sequence

												  ,color

												  ,write_uid

												  ,write_date)

											select id 

												  ,create_uid

												  ,create_date

												  ,name

												  ,sequence

												  ,color

												  ,write_uid

												  ,write_date

				 from odoo9.website_support_ticket_priority  ON CONFLICT(id) DO update set id=excluded.id,create_uid=excluded.create_uid,write_uid=excluded.write_uid,name=excluded.name,create_date=excluded.create_date,write_date=excluded.write_date,sequence=excluded.sequence,color=excluded.color;

	GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(website_support_ticket_priority) odoo11 server from odoo9',cnt;

ALTER TABLE public.website_support_ticket_priority ENABLE TRIGGER ALL;







ALTER TABLE public.res_company_users_rel DISABLE TRIGGER ALL; 

insert into public.res_company_users_rel 

select *from odoo9.res_company_users_rel

 ON CONFLICT(cid,user_id) DO update set user_id=excluded.user_id;

 GET DIAGNOSTICS cnt = ROW_COUNT;

	RAISE NOTICE '% Records inserted into(res_company_users_rel) odoo11 server from odoo9',cnt;

ALTER TABLE public.res_company_users_rel ENABLE TRIGGER ALL; 







end_time:=CLOCK_TIMESTAMP();

age_value:=end_time-start_time;

	RETURN age_value;

	

	exception 

    when others then

        RAISE INFO 'Error Name:%',SQLERRM;

        RAISE INFO 'Error State:%', SQLSTATE;

        return age_value;

END



$BODY$;
-------------------------------------------------------
-- FUNCTION: public.Odoo9_to_Odoo11();

-- DROP FUNCTION public.Odoo9_to_Odoo11();

-------------------------------------------------------

CREATE OR REPLACE FUNCTION public.Odoo9_to_Odoo11(
	)
    RETURNS interval
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
AS $BODY$

 DECLARE cnt INT DEFAULT 0;
 DECLARE max_id INT DEFAULT 0; 
 DECLARE age_value interval ;
 DECLARE ret_val interval ;
 DECLARE start_time TIME ;
 DECLARE end_time TIME ;
BEGIN
start_time:=CLOCK_TIMESTAMP();


ret_val=public.fdw_connect_setup('192.168.0.181', '5432', 'odoo9_14062018', 'postgres', 'root123', 'public', 'odoo9');
RAISE NOTICE 'Postgres_FDW executed successfully in the span of : % ',ret_val;
IF ret_val IS NOT NULL  THEN 
	ret_val=public.emp_module_function();
	RAISE NOTICE 'Employee module function completed in the span of : % ',ret_val;
	ret_val=public.leaves_module_function();
	RAISE NOTICE 'Leave module function completed  in the span of : % ',ret_val;
	ret_val=public.sprint_module_function();
	RAISE NOTICE 'Sprint module function completed in the span of : % ',ret_val;
END IF;




select max(id)+1 into max_id from  public.mail_alias;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.mail_alias_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for mail_alias, now start with %\n',max_id;
END IF;

select max(id)+1 into max_id from  public.res_users;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.res_users_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for res_users, now start with %\n',max_id;
END IF;

select max(id)+1 into max_id from  public.hr_department;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_department_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_department, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.hr_employee;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_employee_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_employee, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.resource_resource;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.resource_resource_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for resource_resource, now start with %',max_id;
END IF;

 select max(id)+1 into max_id from  public.res_partner;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.res_partner_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for res_partner, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.hr_job;	
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_job_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_job, now start with %',max_id+1;
END IF;


select max(id)+1 into max_id from  public.hr_employee_category;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_employee_category_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.res_company;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.res_company_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for res_company, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.account_analytic_line;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.account_analytic_line_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for account_analytic_line, now start with %',max_id+1;
END IF;


select max(id)+1 into max_id from  public.res_config_settings;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.res_config_settings_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for res_config_settings, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.calendar_event;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.calendar_event_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for calendar_event, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.calendar_contacts;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.calendar_contacts_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for calendar_contacts, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.bus_presence;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.bus_presence_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for bus_presence, now start with %',max_id+1;
END IF;

RAISE NOTICE '******************** EMP_MODULE SEQUENCE CONFIGURATION COMPLETED **********************';

select max(id)+1 into max_id from  public.hr_holidays;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_holidays_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_holidays, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.hr_compoff;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_compoff_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_compoff, now start with %',max_id+1;
END IF;


select max(id)+1 into max_id from  public.hr_holidays_status;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_holidays_status_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_holidays_status, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.hr_holidays_summary_dept;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_holidays_summary_dept_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_holidays_summary_dept, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.hr_holidays_summary_employee;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.hr_holidays_summary_employee_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for hr_holidays_summary_employee, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.resource_calendar_leaves;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.resource_calendar_leaves_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for resource_calendar_leaves, now start with %',max_id+1;
END IF;

select max(id)+1 into max_id from  public.account_analytic_account;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.account_analytic_account_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for account_analytic_account, now start with %',max_id+1;
END IF;

RAISE NOTICE '******************** LEAVE MODULE SEQUENCE CONFIGURATION COMPLETED **********************';

select max(id)+1 into max_id from  public.resource_calendar;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.resource_calendar_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for resource_calendar, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.ir_attachment;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.ir_attachment_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for ir_attachment, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.project_task_type;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.project_task_type_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for project_task_type, now start with %',max_id;
END IF;


select max(id)+1 into max_id from  public.project_task;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.project_task_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for project_task, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.project_sprint;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.project_sprint_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for project_sprint, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.project_scrum_team;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.project_scrum_team_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for project_scrum_team, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.mail_template;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.mail_template_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for mail_template, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.project_tags;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.project_tags_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for project_tags, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.project_project;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.project_project_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for project_project, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.mail_message;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.mail_message_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for mail_message, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.mail_message_subtype;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.mail_message_subtype_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for mail_message_subtype, now start with %',max_id;
END IF;

RAISE NOTICE '******************** SPRINT AND PROJECT MODULE SEQUENCE CONFIGURATION COMPLETED **********************';

select max(id)+1 into max_id from  public.website_support_ticket;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.website_support_ticket_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for website_support_ticket, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.website_support_ticket_categories;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.website_support_ticket_categories_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for website_support_ticket_categories, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.website_support_ticket_priority;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.website_support_ticket_priority_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for website_support_ticket_priority, now start with %',max_id;
END IF;


RAISE NOTICE '******************** WEBSITE MODULE SEQUENCE CONFIGURATION COMPLETED **********************';
/*select max(id)+1 into max_id from  public.bus_bus;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.bus_bus_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for bus_bus, now start with %',max_id;
END IF;

select max(id)+1 into max_id from  public.mail_tracking_value;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.mail_tracking_value_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for mail_tracking_value, now start with %',max_id;
END IF;


select max(id)+1 into max_id from  public.mail_mail;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.mail_mail_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for mail_mail, now start with %',max_id;
END IF;


select max(id)+1 into max_id from  public.mail_followers;
IF max_id>1 THEN
	EXECUTE 'ALTER SEQUENCE public.mail_followers_id_seq RESTART WITH '||max_id
	USING max_id;
	RAISE NOTICE 'Sequence changed for mail_followers, now start with %',max_id;
END IF;
RAISE NOTICE '******************** EXTRA TABLES SEQUENCE CONFIGURATION COMPLETED **********************';
*/

DROP schema odoo9 CASCADE;

end_time:=CLOCK_TIMESTAMP();
age_value:=end_time-start_time;
	RETURN age_value;
	
	exception 
    when others then
        RAISE INFO 'Error Name:%',SQLERRM;
        RAISE INFO 'Error State:%', SQLSTATE;
        return age_value;
END

$BODY$;


/*
select public.Odoo9_to_Odoo11()

select public.emp_module_function()

select public.leaves_module_function()

select public.sprint_module_function()
*/