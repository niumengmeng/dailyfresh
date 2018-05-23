# coding=utf-8
from django.db import models


# 购物车表 谁买了几个什么商品
class CartInfo(models.Model):
    user = models.ForeignKey('df_user.userInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField()
