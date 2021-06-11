cd /app/

./manage.py migrate
./manage.py collectstatic

gunicorn -w 3 avgregister.wsgi --bind 0.0.0.0