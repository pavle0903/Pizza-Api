# gunicorn_config.py
bind = '0.0.0.0:8000'
workers = 4
worker_class = 'sync' #ok je da bude sync jer je low-traffic, za produkciju bi bilo dobro namestiti nekog async workera: gevent/eventlet(pip install)