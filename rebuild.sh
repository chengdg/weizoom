mysql -u card --password=weizoom card < rebuild_database.sql
python manage.py syncdb --noinput