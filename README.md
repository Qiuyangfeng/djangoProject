基于django实现，简单的服务器密码管理demo

1.安装库

pip install -r requirements.txt


2.启动项目

python manage.py runserver


3.网页访问

http://127.0.0.1/account/login

默认账号: admin
默认密码：123456

部署项目

使用gunicorn

pip install gunicorn

gunicorn djangoProject.wsgi -b 0.0.0.0:8000

使用uwsgi

pip install uwsgi

uwsgi --http :8000 --file djangoProject/wsgi.py
