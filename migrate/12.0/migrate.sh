echo "migrate database"
mysql -u weapp --password=weizoom weapp < migrate.sql
echo "run deploy_product_model command"
cd ../../weapp
python manage.py syncdb
python manage.py deploy_product_model
python manage.py deploy_refactor_template
