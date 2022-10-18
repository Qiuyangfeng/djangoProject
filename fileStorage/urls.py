from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'fileStorage'
urlpatterns = [
    # 账号密码
    path('', views.file_list, name='file_list'),
    re_path(r'^file/upload1/$', views.file_upload, name='form_upload'),
    re_path(r'^file/upload2/$', views.model_form_upload, name='model_form_upload'),
    path(r'ajax/', views.ajax_upload, name='ajax_upload'),
]
