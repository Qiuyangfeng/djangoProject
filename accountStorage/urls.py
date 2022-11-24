from django.contrib import admin
from django.urls import path, re_path
from accountStorage.views import login, account, server

app_name = 'accountStorage'
urlpatterns = [
    # 登录
    path('login/', login.login, name='login'),
    path('logout/', login.logout, name='logout'),
    path('image/code/', login.image_code, name='image_code'),
    # 账号密码列表
    path('list/', account.account_list, name='account_list'),
    path('add/', account.account_add, name='account_add'),
    path('detail/', account.account_detail, name='account_detail'),
    path('edit/', account.account_edit, name='account_edit'),
    path('delete/', account.account_delete, name='account_delete'),
    # 账号模板上传
    path('ajax/', account.upload_ajax_excel, name='upload_ajax_excel'),
    # 服务器列表
    path('server/', server.server_list, name='server_list'),
    path('server/add/', server.server_add, name='server_add'),
    path('server/detail/', server.server_detail, name='server_detail'),
    path('server/edit/', server.server_edit, name='server_edit'),
    path('server/delete/', server.server_delete, name='server_delete'),
    # 服务器模板上传
    path('server/upload/', server.upload_ajax_excel, name='server_upload'),

]
