# MAD2
python app.py

npm run serve

redis-server

celery -A app.celery_app worker --loglevel=INFO

celery -A app.celery_app beat --loglevel=INFO