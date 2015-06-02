ECHO creating the database for the watchdog
mysql -u weapp --password=weizoom < init_db\rebuild_watchdog.sql
python manage.py syncdb --database=watchdog
