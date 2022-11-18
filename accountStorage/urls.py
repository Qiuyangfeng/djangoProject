from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'accountStorage'
urlpatterns = [
    # 登录
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('image/code/', views.image_code, name='image_code'),
    # 账号密码列表
    path('', views.account_list, name='account_list'),
    path('add/', views.account_add),
    path('detail/', views.account_detail),
    path('edit/', views.account_edit),
    path('delete/', views.account_delete, name='account_delete'),
    # 模板上传
    path('ajax/', views.upload_ajax_excel, name='upload_ajax_excel'),
]
