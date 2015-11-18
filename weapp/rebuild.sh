cd init_db
mysql -h db.weapp.com -u weapp --password=weizoom < rebuild_database.sql
cd ..
python manage.py clean_mongo
python manage.py syncdb --noinput
cd init_db
mysql -h db.weapp.com -u weapp --password=weizoom weapp < loc.sql
cd ..

python manage.py markettool2app
python manage.py init_customized_apps

redis-cli -n 1 -h redis.weapp.com flushdb
