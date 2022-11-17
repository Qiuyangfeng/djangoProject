from django.contrib import admin
from .models import AccountPassword, ServerInfo, AdminUser

admin.site.register(AccountPassword)
admin.site.register(ServerInfo)
admin.site.register(AdminUser)