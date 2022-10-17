from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'accountStorage'
urlpatterns = [
    # 账号密码
    path('', views.account_list, name='account_list'),
    path('add/', views.account_add),
    path('detail/', views.account_detail),
    path('edit/', views.account_edit),
    path('delete/', views.account_delete),
    # 上传列表
    #path('file/', views.file_list, name='file_list'),
    #path('excel/', views.upload_excel, name='upload_excel'),
    # re_path(r'^file/upload1/$', views.file_upload, name='file_upload'),
    # re_path(r'^file/upload2/$', views.model_form_upload, name='model_form_upload'),
    # re_path(r'^file/excel/$', views.upload_excel, name='upload_excel'),
    path('ajax/', views.upload_ajax_excel, name='upload_ajax_excel'),
]
