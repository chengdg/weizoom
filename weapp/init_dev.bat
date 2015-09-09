python manage.py syncdb --noinput
cd init_db
mysql -u weapp --password=weizoom weapp < loc.sql
pause
