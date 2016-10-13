PORT=${1:-8000}
cd devenv/register_service
python run.py --port $PORT
cd ../..
python manage.py runserver 0.0.0.0:$PORT