export LANG=zh_CN.UTF-8
nohup python3 manage.py runserver 0:8012 --noreload >> logs/start.log 2>&1 &