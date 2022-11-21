from django.contrib import admin
from django.urls import path, re_path
from accountStorage.views import login,account,server

app_name = 'accountStorage'
urlpatterns = [
    # 登录
    path('login/', login.login, name='login'),
    path('logout/', login.logout, name='logout'),
    path('image/code/', login.image_code, name='image_code'),
    # 账号密码列表
    path('', account.account_list, name='account_list'),
    path('add/', account.account_add),
    path('detail/', account.account_detail),
    path('edit/', account.account_edit),
    path('delete/', account.account_delete, name='account_delete'),
    # 模板上传
    path('ajax/', account.upload_ajax_excel, name='upload_ajax_excel'),
    # 服务器列表

]
