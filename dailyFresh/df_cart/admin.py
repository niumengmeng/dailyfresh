from django.contrib import admin
from .models import *


class CartInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'goods_id', 'count']


admin.register(CartInfo, CartInfoAdmin)
