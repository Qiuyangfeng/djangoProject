"""PasswordManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from accountStorage import views

app_name = 'accountStorage'
urlpatterns = [
    path('admin/', admin.site.urls),
    # 账号密码
    path('', views.account_list),
    path('add/', views.account_add),
    path('detail/', views.account_detail),
    path('edit/', views.account_edit),
    path('delete/', views.account_delete),
    # 上传列表
    path('file/', views.file_list, name='file_list'),
    path('excel/', views.upload_excel, name='upload_excel'),
    re_path(r'^file/upload1/$', views.file_upload, name='file_upload'),
    re_path(r'^file/upload2/$', views.model_form_upload, name='model_form_upload'),
    re_path(r'^file/excel/$', views.upload_excel, name='upload_excel'),
    path('ajax/', views.upload_ajax_excel, name='upload_ajax_excel'),
]
