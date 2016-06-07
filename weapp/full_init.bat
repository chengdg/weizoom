behave -k -t @full_init
python manage.py init_simulator_user
python manage.py init_customized_apps

mysql -D weapp -u weapp --password=weizoom < init_db\import_sent_messages.sql
