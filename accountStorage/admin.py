from django.contrib import admin
from .models import AccountPassword, ServerInfo

admin.site.register(AccountPassword)
admin.site.register(ServerInfo)