from django.contrib import admin
from .models import *


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['oid', 'user_id', 'odate', 'oIsPay', 'ototal', 'oaddress']


class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods_id', 'order_id', 'price', 'count', ]


admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(OrderDetailInfo, OrderDetailInfoAdmin)