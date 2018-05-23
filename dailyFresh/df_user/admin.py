from django.contrib import admin

from django.contrib import admin
from .models import *


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'uname', 'upwd', 'uemail', 'ushou', 'uaddress', 'uyoubian', 'uphone']


admin.site.register(userInfo, UserInfoAdmin)
