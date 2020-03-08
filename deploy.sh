systemctl restart mariadb.service
gunicorn -c ./config/gunicorn.conf.py wsgi:app