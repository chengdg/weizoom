use weapp;
set SQL_SAFE_UPDATES = 0; 
update account_user_profile set webapp_type=1 where user_id in (select id from auth_user where username='jobs');
update account_user_profile set webapp_type=2 where user_id in (select id from auth_user where username='nokia');
set SQL_SAFE_UPDATES = 1; 
