cd init_db
mysql -u weapp --password=weizoom weapp < rebuild_database.sql
cd ..
python manage.py clean_mongo
python manage.py syncdb --noinput
cd init_db
mysql -u weapp --password=weizoom weapp < loc.sql
cd ..
python manage.py markettool2app
python manage.py init_customized_apps
python manage.py init_permissions
pause
