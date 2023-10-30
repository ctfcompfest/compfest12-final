cd /home/compfest12/ 
python manage.py makemigrations 
python manage.py migrate 
python manage.py collectstatic
gunicorn project.wsgi:application --bind 0.0.0.0:8000